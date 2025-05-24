import plotly.express as px
from backend.plot.types import ChartData
from . import IBuilder
import tempfile


class AreaBuilder(IBuilder):
    async def plot(self, chart_data: ChartData, company_name: str) -> str:
        fig = self._build_area_plot(
            chart_data.data, title=chart_data.title, x=chart_data.x, y=chart_data.y
        )
        # Save to a temporary HTML file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            fig.write_html(tmp.name, include_plotlyjs="cdn", full_html=True)
            tmp_path = tmp.name
        url = await self.netlify_agent.upload_html(tmp_path)
        return url

    @staticmethod
    def _build_area_plot(data, title=None, x=None, y=None, **kwargs):
        # plotly.express.area is available in recent versions
        try:
            fig = px.area(data, x=x, y=y, title=title, **kwargs)
        except AttributeError:
            # Fallback for older plotly: use line with fill
            fig = px.line(data, x=x, y=y, title=title, **kwargs)
            fig.update_traces(fill="tozeroy")
        fig.update_layout(template="plotly_white")
        return fig
