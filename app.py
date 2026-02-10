import feedparser
import streamlit as st
from datetime import datetime
import time

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

# Mock LLM API 调用函数
def summarize_text(text):
    """
    调用 LLM API 进行文本总结（目前使用 Mock 数据）

    Args:
        text (str): 需要总结的文本

    Returns:
        str: 总结后的文本
    """
    # 这里是 Mock 数据，实际使用时替换为真实的 API 调用
    mock_summary = f"""
    [AI 总结] 本文主要研究了人工智能领域的前沿进展。论文提出了创新性的方法，
    在相关任务上取得了显著的性能提升。研究结果表明，该方法具有很好的
    应用前景和实用价值。作者通过充分的实验验证了其有效性，为该领域
    的发展做出了重要贡献。
    """
    return mock_summary.strip()

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

def display_paper(paper):
    """
    显示单篇论文的信息

    Args:
        paper (dict): 论文信息字典
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
        with st.spinner("正在生成总结..."):
            time.sleep(1)  # 模拟 API 调用延迟
            summary = summarize_text(paper['summary'])
            st.write(summary)

# 主界面
def main():
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")

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
            display_paper(paper)
    else:
        st.warning("未能获取到论文数据，请检查网络连接或稍后重试。")

# 运行应用
if __name__ == "__main__":
    main()