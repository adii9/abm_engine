from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel

class QualificationResult(BaseModel):
    icp_fit: bool
    reason: str

@CrewBase
class QualificationCrew():
    """Qualification crew"""

    @agent
    def account_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['account_scout'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @task
    def account_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['account_selection_task'],
            output_pydantic=QualificationResult
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Qualification crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
