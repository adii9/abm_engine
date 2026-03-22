from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel

class ContentResult(BaseModel):
    engagement_plan: str
    value_gift: str
    outreach_email: str

def validate_email_length(result: ContentResult):
    """
    Function-Based Guardrail to ensure the outreach email is under 100 words.
    """
    email_text = result.outreach_email
    word_count = len(email_text.split())
    
    if word_count > 100:
        return (False, f"Error: Email exceeds 100 words (currently {word_count} words). Rewrite to be more concise.")
    
    return (True, result)

@CrewBase
class ContentCrew():
    """Content crew"""

    @agent
    def strategic_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['strategic_copywriter'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_generation_task'],
            output_pydantic=ContentResult,
            guardrail=validate_email_length
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Content crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
