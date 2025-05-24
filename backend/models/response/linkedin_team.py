from pydantic import BaseModel
from typing import Optional, List
from backend.plot.types import ChartData
from backend.models.response.base import CitationResponse


# --- Team Overview ---
class TeamRoleBreakdown(BaseModel):
    role: str
    count: int
    percentage: Optional[float] = None  # Added field for distribution percentage
    sources: Optional[List[int]] = (
        None  # Changed to List[int] for indexing into outer sources
    )
    confidence: Optional[float] = None


class TeamOverviewResponse(CitationResponse):
    company_name: str
    company_description: Optional[str] = None  # Added field for company context
    total_employees: int
    roles_breakdown: List[TeamRoleBreakdown]
    locations: Optional[List[str]] = None
    key_hiring_areas: Optional[List[str]] = None  # Added field for current hiring focus
    growth_rate: Optional[float] = None  # Added field for team expansion rate
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string
    plot_url: Optional[str] = None

    def get_plot_data(self) -> ChartData:
        data = [
            {
                "role": r.role,
                "count": r.count,
                "percentage": r.percentage,
            }
            for r in self.roles_breakdown
        ]
        return ChartData(
            data=data,
            title=f"Team Roles Breakdown for {self.company_name}",
            x="role",
            y="count",
            kind="pie",
        )


# --- Individual Performance ---
class IndividualPerformanceMetric(BaseModel):
    metric: str
    value: float
    sources: Optional[List[int]] = (
        None  # Changed to List[int] for indexing into outer sources
    )
    confidence: Optional[float] = None


class PreviousCompany(BaseModel):
    name: str
    title: str
    duration: Optional[str] = None
    dates: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    dates: Optional[str] = None


class IndividualPerformanceResponse(CitationResponse):
    company_name: str
    individual_name: str
    title: Optional[str] = None
    image_url: Optional[str] = None  # Added field for profile image
    tenure_years: Optional[float] = None
    performance_metrics: List[IndividualPerformanceMetric]
    previous_companies: Optional[List[PreviousCompany]] = (
        None  # Added field for work history
    )
    key_strengths: Optional[List[str]] = None  # Added field for core capabilities
    development_areas: Optional[List[str]] = (
        None  # Added field for growth opportunities
    )
    education: Optional[List[Education]] = None  # Added field for background context
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string
    plot_url: Optional[str] = None

    def get_plot_data(self) -> ChartData:
        data = [
            {"metric": m.metric, "value": m.value} for m in self.performance_metrics
        ]
        return ChartData(
            data=data,
            title=f"Performance Metrics for {self.individual_name}",
            x="metric",
            y="value",
            kind="bar",
        )


# --- Org Structure ---
class OrgNode(BaseModel):
    name: str
    title: str
    department: Optional[str] = None  # Added field for organizational grouping
    linkedin_url: Optional[str] = None  # Added field for direct profile access
    reports_to: Optional[str] = None
    direct_reports: Optional[List[str]] = None
    sources: Optional[List[int]] = (
        None  # Changed to List[int] for indexing into outer sources
    )


class Department(BaseModel):
    name: str
    head: Optional[str] = None
    employee_count: Optional[int] = None
    sub_departments: Optional[List[str]] = None


class LeadershipTeamMember(BaseModel):
    name: str
    title: str
    linkedin_url: Optional[str] = None
    department: Optional[str] = None


class OrgStructureResponse(CitationResponse):
    company_name: str
    org_chart: List[OrgNode]
    ceo: Optional[str] = None  # Added field to highlight top leadership
    departments: Optional[List[Department]] = (
        None  # Added field to show organizational divisions
    )
    leadership_team: Optional[List[LeadershipTeamMember]] = (
        None  # Added field to highlight key executives
    )
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string
    plot_url: Optional[str] = None

    def get_plot_data(self) -> ChartData:
        if self.departments:
            data = [
                {"department": d.name, "employee_count": d.employee_count or 0}
                for d in self.departments
            ]
            return ChartData(
                data=data,
                title=f"Department Sizes for {self.company_name}",
                x="department",
                y="employee_count",
                kind="bar",
            )
        else:
            return ChartData(data=[], title="No department data", kind="bar")


# --- Team Growth ---
class TeamGrowthTimeSeriesPoint(BaseModel):
    period_start: str  # ISO format date string
    period_end: str  # ISO format date string
    hires: int
    attrition: int
    net_growth: int
    growth_rate: Optional[float] = None  # Added field for growth rate at each point
    sources: Optional[List[int]] = (
        None  # Changed to List[int] for indexing into outer sources
    )
    confidence: Optional[float] = None


class DepartmentAttrition(BaseModel):
    department: str
    attrition_count: int
    attrition_rate: Optional[float] = None


class HiringTrendSupportingData(BaseModel):
    """Supporting data for hiring trends with defined properties instead of Dict[str, Any]"""

    percentage: Optional[float] = None
    count: Optional[int] = None
    year_over_year_change: Optional[float] = None
    previous_value: Optional[float] = None
    current_value: Optional[float] = None
    description: Optional[str] = None


class HiringTrend(BaseModel):
    trend: str
    description: str
    supporting_data: Optional[HiringTrendSupportingData] = None


class TeamGrowthResponse(CitationResponse):
    company_name: str
    team_growth_timeseries: List[TeamGrowthTimeSeriesPoint]
    total_hires: int
    total_attrition: int
    net_growth: int
    growth_rate_annualized: Optional[float] = (
        None  # Added field for year-over-year comparison
    )
    key_hiring_areas: Optional[List[str]] = (
        None  # Added field to show focus of recent growth
    )
    attrition_by_department: Optional[List[DepartmentAttrition]] = (
        None  # Added field for deeper analysis
    )
    hiring_trends: Optional[List[HiringTrend]] = (
        None  # Added field to show directional changes
    )
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string
    plot_url: Optional[str] = None

    def get_plot_data(self) -> ChartData:
        data = [
            {"period_start": t.period_start, "net_growth": t.net_growth}
            for t in self.team_growth_timeseries
        ]
        return ChartData(
            data=data,
            title=f"Team Net Growth Over Time for {self.company_name}",
            x="period_start",
            y="net_growth",
            kind="line",
        )
