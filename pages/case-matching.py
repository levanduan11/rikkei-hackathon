import streamlit as st
import sys
import os

# TODO: Thêm các import cho dữ liệu thật
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_pinecone import PineconeVectorStore
# from pymongo import MongoClient
# from langchain.schema import HumanMessage, SystemMessage
# import asyncio
# import nest_asyncio
# from agents import Agent, Runner, WebSearchTool, set_default_openai_client, set_tracing_disabled
# from openai import AsyncOpenAI
# from pydantic import BaseModel, Field

# TODO: Khởi tạo kết nối cho dữ liệu thật
# Initialize MongoDB connection
# mongoClient = MongoClient(st.secrets["MONGO_URI"])
# db = mongoClient["rikkei"]
# caseStudyCollection = db["casestudy"]

# Khởi tạo embeddings cho tìm kiếm vector
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-large",
#     api_key=st.secrets["OPENAI_API_KEY"]
# )

# Khởi tạo vector store cho tìm kiếm case study
# docsearch = PineconeVectorStore.from_existing_index(
#     index_name=st.secrets["PINECONE_INDEX_NAME"],
#     embedding=embeddings,
#     namespace=st.secrets["PINECONE_NAMESPACE"],
# )

# Khởi tạo LLM cho việc tạo đề xuất
# llm = ChatOpenAI(
#     base_url=st.secrets["DEEPSEEK_BASE_URL"],
#     openai_api_key=st.secrets["DEEPSEEK_API_KEY"],
#     model_name=st.secrets["DEEPSEEK_MODEL"],
#     temperature=1,
#     streaming=True
# )

# Khởi tạo agent tìm kiếm công ty
# custom_client = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# set_default_openai_client(custom_client)
# set_tracing_disabled(disabled=True)

# Khởi tạo agent tìm kiếm
# agent = Agent(
#     name="Assistant",
#     instructions="あなたはどの会社に関する情報を検索する専門家です。",
#     model="gpt-4o-mini",
#     tools=[WebSearchTool(
#         user_location={"type": "approximate", "country": "JP", })],
#     output_type=CompanyInfo,
# )

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.matching_data import companies, case_matchings

# from models import CompanyInfo,CaseMatchingInfo

st.set_page_config(layout="wide", page_title="Case Studies Matching")

st.markdown(
    """
<style>
    .company-card {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .company-header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .info-label {
        font-weight: bold;
        color: #333;
        margin: 12px 0;
        font-size: 16px;
    }
    .location-tag {
        background-color: #FFDC5E;
        padding: 8px 15px;
        margin-right: 10px;
        margin-bottom: 8px;
        border-radius: 20px;
        display: inline-block;
        font-size: 14px;
    }
    .match-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        display: inline-block;
        margin-top: 15px;
        margin-bottom: 15px;
        width: 100%;
    }
    .case-box {
        background-color: #e9f7ef;
        border-left: 5px solid #28a745;
        padding: 0;
        margin: 15px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .case-title {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        padding: 12px 15px;
        margin: 0;
        font-size: 16px;
    }
    .case-content {
        padding: 15px;
    }
    .recommendation-box {
        background-color: #e6f3ff;
        border-left: 5px solid #0275d8;
        padding: 15px;
        border-radius: 5px;
    }
    p {
        margin: 12px 0;
        line-height: 1.5;
        font-size: 16px;
    }
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    .streamlit-expanderContent {
        padding-top: 10px;
    }
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        padding-top: 12px;
        padding-bottom: 12px;
    }
    
    p.tag-paragraph {
        margin: 0;
        display: flex;
        align-items: center;
        min-height: 48px;
    }
    
    .info-label {
        font-weight: bold;
        color: #333;
        margin: 12px 0;
        font-size: 16px;
        line-height: 1.5;
        display: flex;
        align-items: center;
        height: 48px;
    }
    .stButton > button {
        background-color: #f44336 !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: 500 !important;
        padding: 8px 27px !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #e53935 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 0.2rem rgba(244, 67, 54, 0.5) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<h5 style="font-weight: 500; margin-bottom: 10px; color: #546e7a; font-size: 18px;">
   顧客ポートフォリオを検索し、ケーススタディを一致させる
</h5>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input(
        "顧客情報（名前、コードなど）", "SCSK", label_visibility="collapsed"
    )
    
with col2:
    search_clicked = st.button("🔍検索", type="primary")

if "active_company" not in st.session_state:
    st.session_state.active_company = None

if "filtered_companies" not in st.session_state:
    st.session_state.filtered_companies = companies

if search_clicked:
    # TODO: Thay thế dữ liệu thật
    # Real data integration:
    # with st.spinner("会社情報を検索中..."):
    #     agent_result = Runner.run_sync(
    #         agent, f'"{search_query}" はある会社に関連する情報です。この会社についての他の情報を検索し、私のアウトソーシングIT会社との協力の方向性を見つけてください。')
    #     
    #     # Convert agent result to company dict format
    #     company_info = agent_result.final_output
    #     company = {
    #         "company_name": company_info.company_name,
    #         "capital": company_info.capital,
    #         "number_of_staff": company_info.number_of_staff,
    #         "scope_of_business": company_info.scope_of_business,
    #         "branches_location": company_info.branches_location,
    #         "revenue": company_info.revenue,
    #         "recruitment_situation": company_info.recruitment_situation,
    #         "summary": company_info.summary
    #     }
    #     st.session_state.filtered_companies = [company]

    # Dữ liệu giả
    query = search_query.lower()
    st.session_state.filtered_companies = [
        company
        for company in companies
        if query in company.get("company_name", "").lower()
        or query in company.get("scope_of_business", "").lower()
        or query in company.get("branches_location", "").lower()
    ]

    if len(st.session_state.filtered_companies) == 0:
        st.warning(f"一致する会社が見つかりませんでした。")

st.markdown(
    """
    <div style="margin: 10px 0 10px 0;">
        <h2 style="
            color: #3f51b5;
            font-weight: 500;
            font-size: 24px;
            border-bottom: 2px solid #3f51b5;
            padding-bottom: 8px;
            display: inline-block;
            position: relative;
        ">
            検索結果
            <span style="
                position: absolute;
                bottom: -2px;
                left: 0;
                width: 50px;
                height: 2px;
                background-color: #ff5722;
            "></span>
        </h2>
    </div>
    """,
    unsafe_allow_html=True,
)


def display_company(idx, company):
    """
    Hàm hiển thị thông tin của công ty
    Args:
        idx (int): Index của công ty trong danh sách
        company (dict): Thông tin của công ty
    """
    with st.expander(f"{company['company_name']}", expanded=True):
        tabs = st.tabs(["会社概要", "事業内容", "所在地"])

        with tabs[0]:
            st.markdown(
                """
            <div style="background-color: #FFFFFF; border-radius: 4px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); margin-bottom: 16px;">
                <h3 style="color: #3f51b5; font-weight: 500; font-size: 20px; margin-bottom: 24px;">
                    会社概要
                </h3>
                <table style="width: 100%; border-collapse: collapse; border: none;">
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="width: 30%; font-weight: 500; color: #666; font-size: 15px; padding: 16px 0; border: none;">会社名</td>
                        <td style="width: 70%; color: rgba(0,0,0,0.87); font-size: 15px; padding: 16px 0; border: none;">{}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="width: 30%; font-weight: 500; color: #666; font-size: 15px; padding: 16px 0; border: none;">資本金</td>
                        <td style="width: 70%; color: rgba(0,0,0,0.87); font-size: 15px; padding: 16px 0; border: none;">{}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="width: 30%; font-weight: 500; color: #666; font-size: 15px; padding: 16px 0; border: none;">従業員数</td>
                        <td style="width: 70%; color: rgba(0,0,0,0.87); font-size: 15px; padding: 16px 0; border: none;">{}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="width: 30%; font-weight: 500; color: #666; font-size: 15px; padding: 16px 0; border: none;">売上高</td>
                        <td style="width: 70%; color: rgba(0,0,0,0.87); font-size: 15px; padding: 16px 0; border: none;">{}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="width: 30%; font-weight: 500; color: #666; font-size: 15px; padding: 16px 0; border: none;">採用状況</td>
                        <td style="width: 70%; color: rgba(0,0,0,0.87); font-size: 15px; padding: 16px 0; border: none;">{}</td>
                    </tr>
                </table>
            </div>
            """.format(
                    company.get("company_name", "---"),
                    company.get("capital", "---"),
                    company.get("number_of_staff", "---"),
                    company.get("revenue", "---"),
                    company.get("recruitment_situation", "---"),
                ),
                unsafe_allow_html=True,
            )

        with tabs[1]:
            st.markdown(
                """
            <div style="background-color: #FFFFFF; border-radius: 4px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); margin-bottom: 16px;">
                <h3 style="color: #4caf50; font-weight: 500; font-size: 20px; margin-bottom: 16px;">
                    事業活動範囲
                </h3>
                <p style="line-height: 1.6; font-size: 15px; color: rgba(0,0,0,0.87);">{}</p>
            </div>
            """.format(
                    company.get("scope_of_business", "---")
                ),
                unsafe_allow_html=True,
            )

            if company.get("summary"):
                st.markdown(
                    """
                <div style="background-color: #FFFFFF; border-radius: 4px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
                    <h3 style="color: #2196f3; font-weight: 500; font-size: 20px; margin-bottom: 16px;">
                        会社の概要
                    </h3>
                    <p style="line-height: 1.6; font-size: 15px; color: rgba(0,0,0,0.87);">{}</p>
                </div>
                """.format(
                        company.get("summary", "")
                    ),
                    unsafe_allow_html=True,
                )

        with tabs[2]:
            st.markdown(
                """
            <div style="background-color: #FFFFFF; border-radius: 4px; padding: 0px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
                <h3 style="color: #ff9800; font-weight: 500; font-size: 20px; margin-bottom: 24px;">
                    本社・支店所在地
                </h3>
            </div>
            """,
                unsafe_allow_html=True,
            )

            locations = company.get("branches_location", "").split(",")

            location_cols = st.columns(3)

            for i, loc in enumerate(locations):
                if loc.strip():
                    with location_cols[i % 3]:
                        st.markdown(
                            f"""
                        <div style="background-color: #f8f9fa; color: #333333; 
                             border-radius: 30px; padding: 12px 20px; 
                             margin: 8px 0 16px 0;
                             font-size: 15px; text-align: center; 
                             box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                            {loc.strip()}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="display: flex; justify-content: center;">',
                unsafe_allow_html=True,
            )

            if st.button(
                "🎯 Rikkeiのケーススタディとマッチング",
                key=f"match_{idx}",
                type="primary",
                use_container_width=False,
            ):
                st.session_state.active_company = company["company_name"]

            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.active_company == company["company_name"]:
            st.markdown(
                "<div style='margin: 32px 0; border-top: 1px solid #e0e0e0;'></div>",
                unsafe_allow_html=True,
            )
            display_case_studies(company)


def display_case_studies(company):
    """
    Hàm hiển thị case study matching theo công ty
    Args:
        company (dict): Thông tin của công ty
    """
    # TODO: Thay thế dữ liệu thật
    # company_info_str = f"""
    #     **会社名:** {company.get('company_name', '---')}\n
    #     **会社の時価総額:** {company.get('capital', '---')}\n
    #     **会社の従業員数:** {company.get('number_of_staff', '---')}\n
    #     **会社の事業活動範囲:** {company.get('scope_of_business', '---')}\n
    #     **会社の本社や支店の所在地情報:** {company.get('branches_location', '---')}\n
    #     **会社の売上:** {company.get('revenue', '---')}\n
    #     **会社の採用状況:** {company.get('recruitment_situation', '---')}\n
    #     **会社の概要:** {company.get('summary', '---')}
    # """
    # 
    # promtSearch = f"""
    #     これはある会社の情報です： \n
    #     {company_info_str}
    #     \n
    #     この会社とrikkei（リッケイソフト, rikkeisoft）との協力情報を提供してください。
    # """
    # 
    # with st.spinner("関連するケースを検索中..."):
    #     results = docsearch.similarity_search_with_score(query=promtSearch, k=4)
    #     matching_data = {"cases_study": [], "summary": {"recommendations": []}}
    #     
    #     # Process case studies from vector search results
    #     for i, (doc, score) in enumerate(results):
    #         st.progress(score, f"{score*100:.1f}% マッチ度")
    #         fileLink = doc.metadata['originFilePath'].replace(
    #             './casestudy', 'https://pub-0ed76f275ac543f195fb2c0884153262.r2.dev')
    #         st.link_button(
    #             f"{doc.metadata['originFileName']} を開く", fileLink)
    #         
    #         # Find case study in MongoDB
    #         caseStudy = caseStudyCollection.find_one({
    #             "originFilePath": doc.metadata['originFilePath']
    #         })
    #         
    #         if caseStudy:
    #             # Extract and format case study content
    #             title = doc.metadata.get('originFileName', f"ケース {i+1}")
    #             detail = "\n".join(page['gpt4oSemanticText'] for page in caseStudy['pages'])
    #             matching_data["cases_study"].append({"title": title, "detail": detail})
    #             
    #             # Generate recommendations for the first result
    #             if i == 0:
    #                 slides_str = "\n".join(page['gpt4oSemanticText'] for page in caseStudy['pages'])
    #                 prompt_casestudy = f"""
    #                     これはある会社に関する内容です。 \n
    #                     {company_info_str}\n
    #                     これは、ITアウトソーシング会社（rikkei）のケーススタディに関する内容です。\n
    #                     {slides_str}\n
    #                     この会社に適用する3つ以上の推奨事項を作成してください。リストとして出力してください。
    #                 """
    #                 
    #                 llm_response = llm.invoke(prompt_casestudy)
    #                 recommendations = [r.strip() for r in llm_response.content.split("\n") if r.strip()]
    #                 matching_data["summary"]["recommendations"] = recommendations

    # Dữ liệu giả
    matching_data = None
    for matching in case_matchings:
        if matching["company_name"] == company["company_name"]:
            matching_data = matching
            break

    if matching_data:
        st.markdown(
            """
            <div style="margin: 20px 0;">
                <h3 style="
                    color: #28a745;
                    font-weight: 500;
                    font-size: 22px;
                    padding: 12px 20px;
                    background-color: #f8f9fa;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    display: flex;
                    align-items: center;
                    position: relative;
                    overflow: hidden;
                ">
                    <span style="
                        position: absolute;
                        left: 0;
                        top: 0;
                        bottom: 0;
                        width: 6px;
                        background-color: #28a745;
                    "></span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#28a745" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    ケースマッチングの詳細
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i, case in enumerate(matching_data.get("cases_study", [])):
            title = case.get("title", "")
            detail = case.get("detail", "")

            case_key = f"case_{company['company_name']}_{i}"

            if case_key not in st.session_state:
                st.session_state[case_key] = False

            is_expanded = st.session_state[case_key]

            display_text = (
                detail
                if is_expanded
                else (detail[:200] + "..." if len(detail) > 200 else detail)
            )

            st.markdown(
                f"""
                <div class='case-box'>
                    <div class='case-title'>ケース {i+1}: {title}</div>
                    <div class='case-content'>
                        {display_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if len(detail) > 200:
                _, col2, _ = st.columns([3, 1, 3])
                with col2:
                    button_label = "閉じる" if is_expanded else "詳細"
                    if st.button(button_label, key=f"btn_{case_key}"):
                        st.session_state[case_key] = not is_expanded
                        st.cache_data.clear()

                st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

        if "summary" in matching_data and "recommendations" in matching_data["summary"]:
            st.markdown(
                """
                <div style="margin-top: 30px; margin-bottom: 20px; display: flex; align-items: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4668b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;">
                        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                    </svg>
                    <h3 style="color: #4668b9; margin: 0; font-size: 20px; font-weight: 500;">要約 / 推奨事項</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
        
            st.markdown(
                """
                <div style="margin-bottom: 30px; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
                    <div style="background-color: #4668b9; color: white; padding: 15px 20px;">
                        <span style="font-size: 18px; font-weight: 500;">推奨された対策</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            for i, rec in enumerate(matching_data["summary"]["recommendations"]):
                st.markdown(
                    f"""
                    <div style="display: flex; margin-bottom: 20px; padding: 0 15px;">
                        <div style="color: #4668b9; font-weight: bold; font-size: 18px; min-width: 30px;">{i+1}.</div>
                        <div style="font-size: 16px; margin-left: 10px;">{rec}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Hiển thị kết quả tìm kiếm công ty
for i, company in enumerate(st.session_state.filtered_companies):
    display_company(i, company)

