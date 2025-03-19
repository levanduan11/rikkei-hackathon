from pydantic import BaseModel, Field
from typing import Optional

class CompanyInfo(BaseModel):
    """会社情報"""
    company_name: str = Field(description="会社名")
    capital: Optional[str] = Field(description="会社の時価総額")
    number_of_staff: Optional[str] = Field(
        description="会社の従業員数")
    scope_of_business: Optional[str] = Field(
        description="会社の事業活動範囲")
    branches_locations: Optional[str] = Field(
        description="会社の本社や支店の所在地情報")
    revenue: Optional[str] = Field(description="会社の売上")
    recruitment_situation: Optional[str] = Field(
        description="会社の採用状況")
    summary: Optional[str] = Field(
        description="会社の概要")


class CaseMatchingInfo(BaseModel):
    """ケースマッチング情報"""
    title: str = Field(description="タイトル")
    detail: str = Field(description="詳細")
