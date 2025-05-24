import plotly.express as px
from backend.plot.types import ChartData
from . import IBuilder
import tempfile
from backend.agents.netlify import NetlifyAgent


class PieBuilder(IBuilder):
    async def plot(self, chart_data: ChartData, company_name: str) -> str:
        fig = self._build_pie_plot(
            chart_data.data, title=chart_data.title, x=chart_data.x, y=chart_data.y
        )
        # Save to a temporary HTML file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            fig.write_html(tmp.name, include_plotlyjs="cdn", full_html=True)
            tmp_path = tmp.name
        netlify_agent = NetlifyAgent()
        url = await netlify_agent.upload_html(tmp_path)
        return url

    @staticmethod
    def _build_pie_plot(data, title=None, x=None, y=None, color=None, **kwargs):
        fig = px.pie(
            data,
            names=x,
            values=y,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Vivid,
            hole=0.45,  # Donut style
            **kwargs,
        )
        fig.update_traces(
            textinfo="percent+label",
            pull=[0.04] * len(data) if hasattr(data, "__len__") else None,
            marker=dict(line=dict(color="#fff", width=2)),
            hoverinfo="label+percent+value",
        )
        fig.update_layout(
            title_font_size=22,
            title_x=0.5,
            font=dict(family="Inter, Arial", size=15, color="#222"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.7)",
                bordercolor="#E2E2E2",
                borderwidth=1,
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            plot_bgcolor="#fff",
            paper_bgcolor="#fff",
        )
        return fig
