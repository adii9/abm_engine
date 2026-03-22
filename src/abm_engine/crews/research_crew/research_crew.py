from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

@CrewBase
class ResearchCrew():
    """Research crew"""

    @agent
    def people_mapper(self) -> Agent:
        return Agent(
            config=self.agents_config['people_mapper'],
            verbose=True
        )

    @agent
    def intel_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['intel_analyst'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @task
    def buying_committee_mapping_task(self) -> Task:
        return Task(
            config=self.tasks_config['buying_committee_mapping_task'],
        )

    @task
    def signal_harvesting_task(self) -> Task:
        return Task(
            config=self.tasks_config['signal_harvesting_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
