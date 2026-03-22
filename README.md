# Agentic ABM Engine

Welcome to the **Agentic ABM Engine**, powered by [crewAI](https://crewai.com). 

This project orchestrates a multi-stage AI workflow (Flow) that completely automates Account-Based Marketing (ABM) outreach. Instead of generic spam, this engine qualifies target accounts, maps their buying committees, harvests real-time "Why Now?" trigger events, and drafts dangerously relevant, hyper-personalized outreach.

## 🧠 How It Works

The engine resolves a robust State Management pattern via Pydantic mapping across **Three specialized Crews**:

1. **Qualification Crew**: Evaluates your chosen Account against your strict Ideal Customer Profile (ICP). The **Account Scout** is equipped with `SerperDevTool` and `ScrapeWebsiteTool` to actively search Google, Tracxn, and LinkedIn to validate firmographics (e.g., recent funding rounds, team sizes) before making a decision. If the profile is rejected, the flow halts to save time and API costs.
2. **Research Crew**: Executes sequentially to map the Buying Committee and harvest signals. 
   - The **People Mapper** actively searches LinkedIn and Tracxn to retrieve the *actual names* of the decision-makers (Economic Buyer, Champion, Influencer) rather than hallucinating theoretical job titles.
   - The **Intel Analyst** uses the same tools to harvest a highly specific, non-obvious trigger event from the last 90 days.
3. **Content Crew**: Synthesizes the decision-makers and trigger events to output an Engagement Plan, a Value Gift, and an Outreach Email (strictly restricted to <100 words dynamically via a Function-Based Guardrail).

### 💾 State Persistence
The workflow state is automatically persisted locally between executions using CrewAI's `@persist()` SQLite framework. You can inspect previous logic traces and generated outputs by exploring the generated database at: `~/Library/Application Support/abm_engine/flow_states.db` (on macOS).

## 🚀 Installation & Setup

Ensure you have Python `>=3.11` installed to support ONNX runtime evaluation. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

1. Install uv (if you haven't already):
```bash
pip install uv
```

2. Lock and install the project dependencies:
```bash
uv sync   # Or `crewai install`
```

### Configuration

**1. Secret API Keys**
Create a `.env` file at the root of the project and add your API credentials. The engine is natively configured to support Gemini out of the box (with `crewai[google-genai]` installed).

```env
GEMINI_API_KEY=your_gemini_api_key
# OR
OPENAI_API_KEY=your_openai_api_key

# Required for the Research Crew's Intel Analyst
SERPER_API_KEY=your_serper_api_key
```

**2. Define Your Ideal Customer Profile (ICP)**
Modify the `icp.yaml` file located at the root of the project to inject your exact target criteria. The Qualification Crew uses this YAML structure dynamically to reject unqualified accounts.

## ⚡ Running the Engine

To kickstart the entire flow manually, run this from the root directory:

```bash
crewai flow kickoff
# Or via UV
uv run kickoff
```

To visualize the sequential execution and routing of your flow, use the CrewAI plot tool:
```bash
crewai flow plot
```

## 🛠️ Customizing the Crews

- **Qualification**: Adjust the "Ruthless Sales Leader" backstory in `src/abm_engine/crews/qualification_crew/config/agents.yaml`.
- **Research**: Augment mapping or scraping tools in `src/abm_engine/crews/research_crew/research_crew.py`.
- **Content**: Tweak the email length or tone in the custom `validate_email_length` guardrail inside `src/abm_engine/crews/content_crew/content_crew.py`.
