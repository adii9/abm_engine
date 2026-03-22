#!/usr/bin/env python
from typing import Dict, Any, Optional
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, router, start
from .crews.qualification_crew.qualification_crew import QualificationCrew
from .crews.research_crew.research_crew import ResearchCrew
from .crews.content_crew.content_crew import ContentCrew

class ABMState(BaseModel):
    company_name: str = ""
    icp_fit: bool = False
    rejection_reason: str = ""
    buying_committee: dict = {}
    trigger_event: str = ""
    final_content: dict = {}

class ABMEngineFlow(Flow[ABMState]):
    
    @start()
    def qualify_account(self):
        import yaml
        from pathlib import Path
        
        print(f"Starting ABM Engine Flow for {self.state.company_name}")
        
        # Load ICP criteria from root directory
        icp_path = Path(__file__).parent.parent.parent / "icp.yaml"
        icp_criteria = "No explicit ICP loaded."
        if icp_path.exists():
            with open(icp_path, "r") as f:
                # Load and dump to convert it to a string format for the prompt
                icp_criteria = yaml.dump(yaml.safe_load(f), default_flow_style=False)
                
        # Run the Qualification Crew
        result = QualificationCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "icp_criteria": icp_criteria
            }
        )
        
        # Determine ICP fit
        self.state.icp_fit = result.pydantic.icp_fit
        if not self.state.icp_fit:
            self.state.rejection_reason = result.pydantic.reason
            
        return result.pydantic

    @router(qualify_account)
    def check_qualification(self):
        if self.state.icp_fit:
            print("ICP Fit confirmed. Routing to research_phase.")
            return "research_phase"
        else:
            print(f"Failed ICP Fit: {self.state.rejection_reason}. Ending flow.")
            return "end_flow"

    @listen("research_phase")
    def research_account(self):
        print("Executing Research Phase...")
        result = ResearchCrew().crew().kickoff(inputs={"company_name": self.state.company_name})
        # Extract results directly from task outputs since ResearchCrew handles multiple tasks
        self.state.buying_committee = getattr(result.tasks_output[0], 'pydantic', {}).dict() if hasattr(result.tasks_output[0], 'pydantic') and result.tasks_output[0].pydantic else {"summary": result.tasks_output[0].raw}
        self.state.trigger_event = result.tasks_output[1].raw
        return result

    @listen(research_account)
    def generate_content(self):
        print("Executing Content Generation Phase...")
        inputs = {
            "company_name": self.state.company_name,
            "buying_committee": str(self.state.buying_committee),
            "trigger_event": self.state.trigger_event
        }
        result = ContentCrew().crew().kickoff(inputs=inputs)
        
        self.state.final_content = {
            "engagement_plan": result.pydantic.engagement_plan,
            "value_gift": result.pydantic.value_gift,
            "outreach_email": result.pydantic.outreach_email
        }
        print("ABM Flow Complete!")
        return self.state.final_content

    @listen("end_flow")
    def end_flow(self):
        print("Flow ended due to failed qualification.")
        return {"status": "rejected", "reason": self.state.rejection_reason}


def kickoff():
    abm_flow = ABMEngineFlow()
    abm_flow.state.company_name = "Acme Corp" # Default test input, would normally be passed in
    result = abm_flow.kickoff()
    print("Final State:", abm_flow.state.model_dump())

def plot():
    abm_flow = ABMEngineFlow()
    abm_flow.plot()

if __name__ == "__main__":
    kickoff()
