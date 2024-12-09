from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.models.model_provider import ModelWrapper

router = APIRouter()

# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


class ContentAnalysisRequest(BaseModel):
    text: str = Field(..., description="The input text to be analyzed for content quality")


class ContentAnalysisResponse(BaseModel):
    seo_score: int = Field(..., ge=0, le=100, description="SEO optimization score from 0 to 100")
    readability_score: int = Field(..., ge=0, le=100, description="Readability score from 0 to 100")
    engagement_score: int = Field(..., ge=0, le=100, description="Engagement score from 0 to 100")
    keywords: list = Field(..., description="List of keywords identified in the text")


@router.post("/analyze_content/", response_model=ContentAnalysisResponse)
def analyze_content(request: ContentAnalysisRequest):
    """
    Analyze the given text for SEO, readability, engagement scores, and identified keywords.
    """
    prompt = f"""
    Produce a structured analysis of a given text based on SEO Optimization, Readability, Engagement and Keywoards. The output must include scores for each category on a scale of 0 to 100, structured in JSON format.

    ### Guidelines
    - **Understand the Text**: Carefully analyze the input text for SEO relevance, readability, and engagement potential. Ensure the analysis considers common guidelines and best practices for each category.
    - **Provide Detailed Analysis**: Include reasoning before assigning scores. Highlight key strengths and weaknesses in the text based on the three criteria. Ensure the explanation informs the scoring process logically.
    - **Maintain Professional Tone**: Responses should be clear, concise, and professional, avoiding unnecessary verbosity.
    - **Format Consistency**: The output must always adhere to the specified JSON format, ensuring clear separation of categories.

    ### Steps
    1. **Analyze the Text for SEO**:
       - Identify keywords and their density.
       - Evaluate the structure for SEO best practices (e.g., headings, metadata, and proper keyword placement).
       - Assign an SEO Optimization score between 0 and 100.

    2. **Evaluate Readability**:
       - Assess sentence structure, vocabulary complexity, and overall clarity.
       - Consider user comprehension for a general audience.
       - Assign a Readability score between 0 and 100.

    3. **Assess Engagement**:
       - Examine tone, relatability, and appeal to the target audience.
       - Evaluate how the text holds reader interest and encourages action.
       - Assign an Engagement score between 0 and 100.

    4. **Identify Keywords**:
         - List the keywords identified in the text.

    4. **Combine Findings**:
       - Summarize the analysis into three scores and provide a brief rationale for each score.

    ### Output Format
    The output must be a JSON object structured as follows:
    {{
        "seo_score": <integer from 0-100>,
        "readability_score": <integer from 0-100>,
        "engagement_score": <integer from 0-100>
        "keywords": [<list of identified keywords>]
    }}

    ### Notes
    - **Reasoning Before Scoring**: Always evaluate the input text thoroughly and provide reasoning for each score, even if not included in the final output. This ensures consistency and avoids arbitrary scoring.
    - **Edge Cases**: For highly technical or niche texts, adapt readability and engagement criteria to match the expected audience, while maintaining SEO consistency.

    Input Text: {request.text}
    """
    structured_output = llm.with_structured_output(ContentAnalysisResponse)
    analysis_result: ContentAnalysisResponse = structured_output.invoke(prompt)

    return analysis_result
