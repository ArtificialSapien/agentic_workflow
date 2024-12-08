import os
import json
from typing import List
from typing import TypedDict, Union
import requests

from app.models.base import AzureDallE3ImageGenerator
from app.agents.data_models import NewsArticle
from app.models.model_provider import ModelWrapper
from app.agents.data_models import NewsArticles, MemeTemplate, MemeCaptions

from app.helper_functions import fetch_templates
from app.helper_functions import ensure_markdown_format


from dotenv import load_dotenv

from app.web_crawler.news_sources import GoogleNewsSource
from app.web_crawler.query_encoder import QueryEncoder
from app.web_crawler.summarizers import Summarizer, SummarizerUsingGroq

# Load environment variables
load_dotenv(override=True)

# llm = AzureChatOpenAI(deployment_name="gpt-4o-mini")
lim = AzureDallE3ImageGenerator(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    url=os.getenv("AZURE_OPENAI_DALLE3_ENDPOINT"),
)

# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


class AgentState(TypedDict):
    """
    Represents the state of an agent.

    Attributes:
        user_prompt (str): The prompt provided by the user.
        generate_text (bool): Indicates whether text generation is enabled.
        generate_image (bool): Indicates whether image generation is enabled.
        generate_video (bool): Indicates whether video generation is enabled.
        generate_meme (bool): Indicates whether meme generation is enabled.
        news_articles (Union[NewsArticles, None]): The news articles used for generation.
        generated_text (Union[str, None]): The generated text.
        generated_image_url (Union[str, None]): The URL of the generated image.
        generated_video_url (Union[str, None]): The URL of the generated video.
        generated_meme_url (Union[str, None]): The URL of the generated meme.
    """

    user_prompt: str
    content_style: str
    content_format: str
    generate_text: bool
    generate_image: bool
    generate_video: bool
    generate_meme: bool
    news_articles: Union[NewsArticles, None]
    generated_text: Union[str, None]
    generated_image_url: Union[str, None]
    generated_video_url: Union[str, None]
    selected_meme_template: Union[MemeTemplate, None]
    generated_meme_url: Union[str, None]


def load_json_files_from_folder(folder_path: str) -> List[NewsArticle]:
    articles = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                article = NewsArticle(**data)
                articles.append(article)
    return articles


def web_crawler(state: AgentState):
    """"""
    user_prompt = state["user_prompt"]

    # node 1 prompt -> query (using llm)
    # node 2 query -> top 5 results

    # query_encoder = QueryEncoder()
    # news_source = GoogleNewsSource()

    # summarizer: Summarizer = SummarizerUsingGroq()

    # topic = query_encoder.get_topic(state["user_prompt"])

    # news_source.fetch({
    #    "q": topic,
    #    "engine": "google_news",
    #    "gl": "us",
    #    "hl": "en"
    # })
    # limit=os.getenv("MAX_NUMBER_OF_ARTICLES")
    # complete_news_articles = news_source.get_news_content(limit=5)

    # text_to_summarize = """b'Artificial Intelligence Nudges Scientist to Try Simpler Approach to Quantum Entanglement\nSkip to content\nNews\nCapital Markets\nNational\nQuantum Computing Business\nResearch\nExclusives\nEducation\nFeatured\nInsights\nInterviews\nMedia\nReports\nWomen In Quantum\nSolutions\nAbout Us\nMenu\nNews\nCapital Markets\nNational\nQuantum Computing Business\nResearch\nExclusives\nEducation\nFeatured\nInsights\nInterviews\nMedia\nReports\nWomen In Quantum\nSolutions\nAbout Us\nSubscribe\nSignup\nNews\nQuantum Computing Business\nNational\nCapital Markets\nExclusives\nInsights\nEducation\nInterviews\nMedia\nIntro to quantum\nAdvisory\nAbout Us\nMarketing\nQ-munity\nNews\nQuantum Computing Business\nNational\nCapital Markets\nExclusives\nInsights\nEducation\nInterviews\nMedia\nIntro to quantum\nAdvisory\nAbout Us\nMarketing\nQ-munity\nContact Us\nGet demo\nArtificial Intelligence Nudges Scientist to Try Simpler Approach to Quantum Entanglement\nResearch\nMatt Swayne\nDecember 7, 2024\nInsider Brief\nThe team\xe2\x80\x99s new approach avoids starting with pre-entangled pairs or performing Bell-state measurements, relying instead on the indistinguishability of photon paths.\nAn AI tool called PyTheus, originally tasked with reproducing established entanglement-swapping protocols, unexpectedly revealed a simpler method to entangle independent photons.\nThis discovery reduces complexity in quantum networks and challenges long-held assumptions about what is required to generate entanglement at a distance.\nPRESS RELEASE \xe2\x80\x94 Physicists have discovered a simpler way to create quantum entanglement between two distant photons \xe2\x80\x94 without starting with entanglement, without resorting to Bell-state measurements, and even without detecting all ancillary photons \xe2\x80\x94 an advance that challenges long-held assumptions in quantum networking.\nAnd all it took was a friendly nudge from an artificial intelligence tool.\nAn international team of scientists led by researchers from Nanjing University and the Max Planck Institute for the Science of Light described their method in Physical Review Letters \xe2\x80\x94 accessed for this article through arXiv \xe2\x80\x94 that demonstrated entanglement can emerge from the indistinguishability of photon paths alone. Instead of relying on standard procedures that start from prepared entangled pairs and complex joint measurements, their technique leverages a basic quantum principle: when multiple photons could have come from several possible sources, erasing the clues to their origins can produce entanglement where none existed before.\nInterestingly \xe2\x80\x94 and perhaps even more importantly \xe2\x80\x94 this unexpected advance stems from the use of an artificial intelligence tool called PyTheus, initially relied on to rediscover a workhorse protocol in quantum communications known as entanglement swapping. Instead, the algorithm turned up something simpler. According to Mario Krenn, a research group leader of the\xc2\xa0Artificial Scientist Lab\xc2\xa0at the\xc2\xa0Max Planck Institute for the Science of Light, the solution the AI delivered seemed too straightforward at first.\n\xe2\x80\x9cWe discovered this idea coincidentally while applying PyTheus to quantum protocols,\xe2\x80\x9d Krenn wrote on X. \xe2\x80\x9cAs a first task, we aimed to rediscover entanglement swapping, one of the most crucial protocols in quantum networks. Curiously, the algorithm kept producing something else \xe2\x80\x94 something simpler \xe2\x80\x94 which we initially thought was incorrect.\xe2\x80\x9d\nAccording to the paper, entanglement swapping typically requires starting with two separate entangled pairs and performing a special joint measurement \xe2\x80\x94 called a Bell-state measurement \xe2\x80\x94 on one photon from each pair. This collapses the system, leaving the two other photons entangled even though they never interacted directly. It has been a cornerstone of quantum network design for decades. But in their new work, Krenn and his colleagues show there are other ways to achieve a similar end result without this chain of prerequisites.\nBy making all possible paths of photon generation identical, the team\xe2\x80\x99s scheme generates entanglement purely through the quantum uncertainty about origins. Overlooked for more than 25 years, Krenn writes that this simpler approach cuts away complexity. Instead of meticulously preparing entanglement and then using a Bell-state projection to distribute it, the method uses a superposition of different generation events to yield the same effect. This contrasts sharply with decades of conventional wisdom about what\xe2\x80\x99s \xe2\x80\x9crequired\xe2\x80\x9d to create entanglement at a distance.\n\xe2\x80\x9cFor me, this changed my perspective on what is necessary to create entanglement\xe2\x80\x94not because I now know what is necessary, but because we\xe2\x80\x99ve realized what is not,\xe2\x80\x9d Krenn wrote in the social media point.\nExperimentally Sound, Philosophically Intriguing\nThe PyTheus algorithm, according to Krenn, was tasked with re-deriving established protocols like entanglement swapping. Instead, it kept serving up a configuration that demanded less overhead. In classical logic, less resource-intensive often means inferior. But here, the surprising solution turned out to be experimentally sound and philosophically intriguing. Rather than using established building blocks like Bell-state measurements, the new approach exploits indistinguishable photon origins to tie together distant particles. It even allows for scenarios in which not all ancillary photons need to be detected, suggesting that resource requirements in future quantum networks might be lowered.\nIn the researchers\xe2\x80\x99 experiment, no prior entanglement source or measurement apparatus was required. By adjusting the photon sources and ensuring their outputs are indistinguishable, they created conditions where detecting photons at certain paths guaranteed that two others \xe2\x80\x94 never directly interacting \xe2\x80\x94 emerged entangled. This approach could simplify the construction of quantum links between distant locations and reduce the complexity of multi-node quantum networks, making them more scalable and potentially more practical.\nSuch a discovery could have implications for quantum communication and information processing. Quantum networks, aimed at enabling secure message transmission and distributed quantum computing, have long leaned on well-established methods like entanglement swapping. Now, a new generation of protocols may emerge that rely on fundamental quantum principles in more direct ways.\nTo be sure, as with all early-stage quantum demonstrations, scaling this method to realistic network lengths and larger numbers of photons remains a challenge. Environmental noise, losses, and device imperfections still loom large. But now that a previously unrecognized mechanism for generating entanglement has come to light, quantum engineers have fresh avenues to explore.\n\xe2\x80\x9cConventional, AI-discovered solutions are complex and it takes ages to understand what is going on,\xe2\x80\x9d Krenn wrote in his post. \xe2\x80\x9cIn this case, the solution was way simpler than we expected.\xe2\x80\x9d\nThe development underscores that as quantum technologies advance, AI-assisted discovery may be able to partner with human scientists to open up previously unimagined paths. Just as PyTheus inadvertently revealed that entanglement swapping wasn\xe2\x80\x99t the only game in town, future tools may find other hidden protocols that defy conventional wisdom. By stripping away decades-old assumptions, this result prompts researchers to reconsider what truly defines entanglement generation\xe2\x80\x94and what might be possible as they push quantum networks toward practical, wide-scale deployment.\nIndustry Implications?\nAlthough not directly addressed in the paper, the use of AI in identifying simpler, more efficient methods of producing quantum entanglement hints at needed help for the entire quantum computing ecosystem. By moving beyond human intuition and established routines, algorithms like PyTheus can rapidly uncover new protocols that shave down complexity, reduce resource overhead, and streamline quantum experiments.\nThe approach, itself, could also help engineers and researchers achieve more scalable quantum networks faster, laying groundwork not just for advances in secure communication, but for broader innovations in quantum sensors, simulators, and ultimately, practical quantum computers.\nFor a more technical look at the experiment, please review the paper available on Physical Review Letters and on arXiv.\nIn addition to Krenn, the study\xe2\x80\x99s authors include Kai Wang and Zhaohua Hou\xe2\x80\x94who contributed equally\xe2\x80\x94along with Kaiyi Qian, Leizhen Chen, Shining Zhu, and Xiao-Song Ma, all from the National Laboratory of Solid-state Microstructures, School of Physics, and the Collaborative Innovation Center of Advanced Microstructures at Nanjing University in China.\nAIArtificial IntelligenceBell-StateMario KrennPyTheusquantum entanglement\nMatt Swayne\nLinkedIn\nWith a several-decades long background in journalism and communications, Matt Swayne has worked as a science communicator for an R1 university for more than 12 years, specializing in translating high tech and deep tech for the general audience. He has served as a writer, editor and analyst at The Quantum Insider since its inception. In addition to his service as a science communicator, Matt also develops courses to improve the media and communications skills of scientists and has taught courses.\n[email\xc2\xa0protected]\nShare this article:\nRelevant\nMore\nGuest Post:\nThe Unexaggerated Magic of Quantum\nShai Phillips\nJanuary 17, 2024\nError-Mitigation Techniques Can Pump Up The Quantum Volume\nMatt Swayne\nMarch 16, 2022\nHSBC, IBM to Explore Using Quantum Computers for Financial Services\nMatt Swayne\nMarch 31, 2022\nEntropica Labs, Atom Computing Announce Strategic Partnership\nMatt Swayne\nJune 22, 2023\nResearchers Turn an Atomic Microscope into a Quantum\xc2\xa0Computer\nJames Dargan\nOctober 17, 2023\nRecommended\nMore\nQuantum Machine Learning Is The Next Big Thing\nMay 28, 2020\n12 Top Quantum Computing Universities in 2024\nApril 18, 2022\nSifting through the Clouds: Polish Researchers Will Test the Utility of Quantum Algorithms for Satellite Imagery\nMay 24, 2021\nKeep track of everything going on in the Quantum Technology Market.In one place.\nGet started\nRelated Articles\nView all\nGuest Post: Deep Tech Success \xe2\x80\x94 Redefining Your Commercial Strategy for 2025\nMatt Swayne\nDecember 7, 2024\nArtificial Intelligence Nudges Scientist to Try Simpler Approach to Quantum Entanglement\nMatt Swayne\nDecember 7, 2024\nIndia\xe2\x80\x99s National Quantum Mission Invites Israeli Startups: Building Global Partnerships for Quantum Technology\xe2\x80\x99s Future\nCierra Choucair\nDecember 6, 2024\nEY, IBM Guest Post \xe2\x80\x94 Up And Running on Day Two: How Businesses Can Prepare For Quantum\xe2\x80\x99s Promise\nResonance\nDecember 6, 2024\nImproved Performance of Superconducting Qubits Makes Investigation of Sapphire Substrates Compelling as an Alternative to Silicon\nJakob P\nDecember 14, 2023\nGuest Post: Reimagining Primary Care \xe2\x80\x94 Clinical Quantum, AI And The Role of Hackathons in Shaping a New Era For The NHS\nMatt Swayne\nDecember 1, 2024\nFrom Cat Qubits to Universal Quantum Computing: Alice & Bob\xe2\x80\x99s 2030 Roadmap Delivers High-Fidelity Solutions\nCierra Choucair\nDecember 4, 2024\nEntropica Labs and Xanadu Partner to Simplify Fault-Tolerant Quantum Computing\nCierra Choucair\nDecember 3, 2024\nSDT Secures $14.1M Pre-IPO Investment to Advance Korea\xe2\x80\x99s Quantum Technology Leadership\nCierra Choucair\nDecember 5, 2024\nQuantum Insider is the leading provider of media and market intelligence on the quantum technology industry.\nLinkedin-in\nYoutube\nInstagram\nFacebook-f\nTiktok\nFeatured News\nGuest Post: Deep Tech Success \xe2\x80\x94 Redefining Your Commercial Strategy for 2025\nDecember 7, 2024\nArtificial Intelligence Nudges Scientist to Try Simpler Approach to Quantum Entanglement\nDecember 7, 2024\nIndia\xe2\x80\x99s National Quantum Mission Invites Israeli Startups: Building Global Partnerships for Quantum Technology\xe2\x80\x99s Future\nDecember 6, 2024\nGuest Post: Deep Tech Success \xe2\x80\x94 Redefining Your Commercial Strategy for 2025\nDecember 7, 2024\nArtificial Intelligence Nudges Scientist to Try Simpler Approach to Quantum Entanglement\nDecember 7, 2024\nIndia\xe2\x80\x99s National Quantum Mission Invites Israeli Startups: Building Global Partnerships for Quantum Technology\xe2\x80\x99s Future\nDecember 6, 2024\nNavigate\nNews\nExclusives\nMarketing\nAdvisory\nReports\nNews\nExclusives\nMarketing\nAdvisory\nReports\nNews\nExclusives\nMarketing\nAdvisory\nReports\nNews\nExclusives\nMarketing\nAdvisory\nReports\nProjects\nResonance\nDigital Twin Insider\nSpace Impulse\nAI Insider\nClimate Insider\nContact Us\nEmail Us\nLegal\nPrivacy Policy\nTerms and Conditions\nEditorial Policy\n2024 \xc2\xa9Copyright Resonance Alliance Inc. All Rights Reserved\nDesigned by Resonance\nCookies\nWe use cookies to improve your experience on our site. By continuing to browse our site, you consent to our use of cookies. For more details, you can manage your preferences under "Settings".\nRead our cookie policy\nSettings\nAccept all\nCookies\nChoose what kind of cookies to accept. Your choice will be saved for one year.\nRead our cookie policy\nNecessary\nThese cookies are not optional. They are needed for the website to function.\nStatistics\nIn order for us to improve the website\'s functionality and structure, based on how the website is used.\nExperience\nIn order for our website to perform as well as possible during your visit. If you refuse these cookies, some functionality will disappear from the website.\nMarketing\nBy sharing your interests and behavior as you visit our site, you increase the chance of seeing personalized content and offers.\nSave\nAccept all\nSearch for:\n\xc3\x97\nThe weekly QC newsletter\nWelcome to our weekly QC newsletter. Yes, we know we are The Quantum Insider but we also appreciate that you probably don\xe2\x80\x99t want us in your inbox every day. Here is what we have been working on this week.\nYou can unsubscribe anytime. For more details, review our Privacy Policy.\nSubscribe\nLoading\xe2\x80\xa6\nThank you!\nYou have successfully joined our subscriber list.\n\xc3\x97\nThank you!\nOne of our team will be in touch to learn more about your requirements, and provide pricing and access options.\n\xc3\x97\nNews\nQuantum Computing Business\nNational\nCapital Markets\nExclusives\nInsights\nEducation\nInterviews\nMedia\nIntro to quantum\nAdvisory\nAbout Us\nMarketing\nQ-munity\nNews\nQuantum Computing Business\nNational\nCapital Markets\nExclusives\nInsights\nEducation\nInterviews\nMedia\nIntro to quantum\nAdvisory\nAbout Us\nMarketing\nQ-munity\nContact Us\nIntelligence\nSubscribe to our industry leading leading newsletter for the latest in quantum news and insights.\nEmail\nSUBSCRIBE\nJoin Our Newsletter\nYou can unsubscribe anytime. For more details, review our Privacy Policy.\nSubscribe\nLoading...\nThank you!\nYou have successfully joined our subscriber list.\nDigitalagentur Forge12 Interactive GmbH'"""
    # news_articles = []
    # for news_article in complete_news_articles:
    #    short_text = summarizer.get_summary(str(news_article.content))
    #    news_article.content = short_text
    #    news_articles.append(news_article)

    # TODOD creates news articles
    news_articles = load_json_files_from_folder("./data/work/wired/output")
    # news_articles = [NewsArticle(title="cooking class", date="today", content="this is a cooking class story", author="myself", source="whatever.com")]
    return {"news_articles": news_articles}


def text_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    content_style = state["content_style"]
    content_format = state["content_format"]
    prompt = f"""
        You are a social media post creator. Use the provided news articles along
        with the initial user prompt used to collect the news articles to generate
        engaging social media text. Ensure the output reflects the specified format and style/tone.
        # Steps
            1. Review the provided news articles and the initial user prompt.
            2. Extract key points and themes from the articles.
            3. Craft a social media post that aligns with the desired style and tone.
            4. Format the output in Markdown, using appropriate headers, bullet points, and/ or links as needed.
        # Output Format'
            1. The output should be a single social media post formatted in Markdown.
            2. It should be written in the style and tone requested.
            3. It should have the length matching the requested style.
            4. Add references to the text extracted from the news articles field - 'source' in the text as an Markdown upper index at the end the corresponding sentence.
            5. Add all included references to the end of the post as a list of links using the matching indexing - appearance order in the text.
        **Given:**
            1. News Articles: {news_articles}
            2. User Prompt: {user_prompt}
            3. Expected article format: {content_format}
            4. Expected article style: {content_style}
        """
    if state["generate_text"] == True:
        try:
            generated_text: str = llm.invoke(prompt).content.strip()
        except Exception as e:
            generated_text = "LLM model invokation failed - please holder text"

        return {"generated_text": ensure_markdown_format(generated_text)}
    return {"generated_text": "Text generation was not requested"}


def image_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    prompt_for_instructing_image_generation = f"""
        You are a social media post creator.
        **Given:**
            - **News articles:** {news_articles}
            - **User prompt:** {user_prompt}
        **Your objectives are to: **
            1. **Create:**
                - Create a prompt based on the received news articles and initial user prompt to instruct the image generator to create an image.
                - Ensure that the style, content are aligned with the provided context.
        """
    if state["generate_image"] == True:

        try:
            prompt_for_image_generation: str = llm.invoke(
                prompt_for_instructing_image_generation
            ).content
            print(prompt_for_image_generation)

            # Call the image generator API
            lim.generate_image(prompt_for_image_generation)
            if lim.image_generated:
                print("image_was_generated")
                return {"generated_image_url": lim.image_url}
            else:
                return {
                    "generated_image_url": "No image generated due to internal error"
                }
        except Exception as e:
            return {"generated_image_url": "Certain error occured"}

    else:
        return {"generated_image_url": "Image generation was not requested"}


def video_generator(state: AgentState):
    if state["generate_video"] == False:
        return {"generated_video_url": None}

    user_prompt = state["user_prompt"]
    initial_image_url = state["generated_image_url"]
    prompt = f"""
        You are a video creator.
        Given an initial image, your objective is to create a video using Stability AI.

        **Given:**
            - **Initial Image:** {initial_image_url}

        **Your objectives are to:**
            1. **Create:**
                - Create a video using Stability AI based on the initial image.
                - Enhance the visual quality and stability of the video.
                - Add relevant effects and transitions.
    """
    import requests

    response = requests.post(
        f"https://api.stability.ai/v2beta/image-to-video",
        headers={"authorization": f"""Bearer {os.getenv("STABILITY_AI_API_KEY")}"""},
        files={"image": open("../data/test_resized_image3.jpg", "rb")},
        data={"seed": 0, "cfg_scale": 1.8, "motion_bucket_id": 127},
    )

    print("Generation ID:", response.json().get("id"))

    return {"prompt": prompt}


def meme_selector(state: AgentState):
    if state["generate_meme"] == False:
        return {"selected_meme_template": None}

    user_prompt = state["user_prompt"]
    templates = fetch_templates()
    prompt = f"""
        Select the most appropriate meme template based on the provided user prompt: {user_prompt}
        Using the given list of templates: {templates}
        Each template is defined by a unique ID, name, URL, width, height, and box count.
        Your task is to analyze the user prompt to identify relevant keywords and themes,
        then match those with the best-fitting template from the list.

        # Steps
        1. **Analyze User Prompt**: Break down the user prompt to identify key themes and keywords.
        2. **Match Keywords with Templates**: Compare the identified keywords with the names of the templates to find the most relevant match.
        3. **Select Appropriate Template**: Choose the template that most closely aligns with the user's prompt.
        4. **Format the Output**: Structure the output to include the template's unique ID, name, URL, width, height, and box count.
    """
    structure_llm = llm.with_structured_output(MemeTemplate)
    selected_meme_template: MemeTemplate = structure_llm.invoke(prompt)
    return {"selected_meme_template": selected_meme_template}


def meme_generator(state: AgentState):
    if state["generate_meme"] == False:
        return {"generated_meme_url": None}

    user_prompt = state["user_prompt"]
    meme_template = state["selected_meme_template"]
    box_count = meme_template.box_count
    prompt = f"""
        You are an AI assistant. Given a user prompt and given meme template, select the
        most appropriate meme captions. The number of meme captions required will be based
        on the number of text boxes in the meme template {box_count}.

        User Prompt: "{user_prompt}"
        Meme Template: "{meme_template}"
        Box Counts: "{box_count}"

    """
    structure_llm = llm.with_structured_output(MemeCaptions)
    caption_response = structure_llm.invoke(prompt)

    template_id = meme_template.id
    username = "mmaazkhanhere"
    password = "HelloWorld00."
    box_count = meme_template.box_count

    texts = []

    for i in range(box_count):
        texts.append(caption_response.captions[i])

    url = "https://api.imgflip.com/caption_image"

    # Prepare the payload with the parameters
    payload = {"template_id": template_id, "username": username, "password": password}

    for i in range(box_count):
        payload[f"text{i}"] = texts[i]

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            # Display the meme URL
            return {"generated_meme_url": data["data"]["url"]}
        else:
            return {"generated_meme_url": "failed to generate meme"}
    else:
        return {"generated_meme_url": "Failed to contact Imgflip API."}
