import feedparser
import streamlit as st
from datetime import datetime
import time
from openai import OpenAI

# 页面配置
st.set_page_config(
    page_title="个性化信息总结助手",
    page_icon="📚",
    layout="wide"
)

# 标题
st.title("📚 个性化信息总结助手")
st.markdown("---")

# ArXiv RSS 源配置
ARXIV_RSS_URL = "http://export.arxiv.org/rss/cs.AI"  # AI 领域的 RSS
KEYWORDS = ["Artificial Intelligence", "Machine Learning", "Deep Learning"]

# 智谱 AI 总结函数
def summarize_text(text, api_key):
    """
    调用智谱 AI 进行文本总结

    Args:
        text (str): 需要总结的文本
        api_key (str): 智谱 AI API Key

    Returns:
        str: 总结后的文本，失败时返回 None
    """
    if not api_key:
        return None

    try:
        # 初始化智谱 AI 客户端（OpenAI 兼容模式）
        client = OpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )

        # 调用 API
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的科研论文助手。请将这段摘要翻译成通顺的中文，并以 bullet points 的形式列出 3 条核心创新点。"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # 提取返回的总结
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        raise Exception(f"智谱 API 调用失败: {str(e)}")

def fetch_arxiv_papers():
    """
    抓取 ArXiv 的 RSS 订阅源

    Returns:
        list: 论文列表，每个元素包含标题、作者、摘要、发布日期等信息
    """
    try:
        # 解析 RSS 源
        feed = feedparser.parse(ARXIV_RSS_URL)

        papers = []

        for entry in feed.entries:
            paper = {
                'title': entry.title,
                'authors': [author.name for author in entry.authors] if hasattr(entry, 'authors') else [],
                'summary': entry.summary,
                'published_date': entry.published,
                'link': entry.link,
                'categories': entry.tags if hasattr(entry, 'tags') else []
            }
            papers.append(paper)

        return papers

    except Exception as e:
        st.error(f"抓取 ArXiv 论文时发生错误: {str(e)}")
        return []

def display_paper(paper, api_key):
    """
    显示单篇论文的信息

    Args:
        paper (dict): 论文信息字典
        api_key (str): 智谱 AI API Key
    """
    with st.expander(f"**{paper['title'][:100]}{'...' if len(paper['title']) > 100 else ''}**"):
        # 标题
        st.markdown(f"### 📖 {paper['title']}")

        # 作者和日期
        authors_str = ", ".join(paper['authors'][:3])  # 只显示前3位作者
        if len(paper['authors']) > 3:
            authors_str += f" 等 ({len(paper['authors'])} 位作者)"

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**👤 作者**: {authors_str}")
        with col2:
            if paper['published_date']:
                try:
                    pub_date = datetime.strptime(paper['published_date'], '%a, %d %b %Y %H:%M:%S %Z')
                    st.markdown(f"**📅 发布**: {pub_date.strftime('%Y-%m-%d')}")
                except:
                    st.markdown(f"**📅 发布**: {paper['published_date'][:10]}")

        # 链接
        st.markdown(f"**🔗 [原文链接]({paper['link']})**")

        # 摘要
        st.markdown("#### 📄 摘要")
        st.write(paper['summary'])

        # AI 总结
        st.markdown("#### 🤖 AI 总结")
        if not api_key:
            st.warning("⚠️ 请在侧边栏填写智谱 AI API Key 以启用 AI 总结功能")
        else:
            with st.spinner("正在生成总结..."):
                try:
                    summary = summarize_text(paper['summary'], api_key)
                    if summary:
                        st.write(summary)
                    else:
                        st.warning("⚠️ 总结生成失败")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

# 主界面
def main():
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")

        # 智谱 AI API Key 输入
        st.subheader("🔑 API 设置")
        api_key = st.text_input(
            "智谱 AI API Key",
            type="password",
            help="请输入您的智谱 AI API Key 以启用 AI 总结功能"
        )

        # 显示抓取的论文数量
        st.subheader("📊 统计信息")
        st.metric("关键词", ", ".join(KEYWORDS))
        st.metric("RSS 源", ARXIV_RSS_URL)

        # 刷新按钮
        if st.button("🔄 刷新论文", type="primary"):
            st.rerun()

    # 主体内容
    st.header("📋 最新 AI 论文")

    # 显示加载状态
    with st.spinner("正在抓取 ArXiv 最新论文..."):
        papers = fetch_arxiv_papers()

    # 显示论文数量
    st.info(f"找到 {len(papers)} 篇相关论文")

    # 显示论文列表
    if papers:
        # 搜索框
        search_term = st.text_input("🔍 搜索论文标题或摘要", "")

        # 过滤论文
        filtered_papers = papers
        if search_term:
            filtered_papers = [
                paper for paper in papers
                if search_term.lower() in paper['title'].lower() or
                   search_term.lower() in paper['summary'].lower()
            ]
            st.info(f"找到 {len(filtered_papers)} 篇匹配的论文")

        # 显示论文
        for paper in filtered_papers:
            display_paper(paper, api_key)
    else:
        st.warning("未能获取到论文数据，请检查网络连接或稍后重试。")

# 运行应用
if __name__ == "__main__":
    main()