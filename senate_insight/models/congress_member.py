"""Data models for Congressional members."""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CongressMember(BaseModel):
    """Represents a member of Congress (Senate or House)."""
    
    member_id: str = Field(..., description="Unique identifier for the member")
    name: str = Field(..., description="Full name of the member")
    chamber: str = Field(..., description="Senate or House")
    state: str = Field(..., description="State the member represents")
    district: Optional[str] = Field(None, description="District number (House only)")
    party: str = Field(..., description="Political party affiliation")
    start_date: date = Field(..., description="Start date of current term")
    end_date: Optional[date] = Field(None, description="End date of current term")
    committees: List[str] = Field(default_factory=list, description="Committee memberships")
    leadership_positions: List[str] = Field(default_factory=list, description="Leadership roles")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }


class CommitteeAssignment(BaseModel):
    """Represents a committee assignment for a Congress member."""
    
    member_id: str = Field(..., description="Member identifier")
    committee_name: str = Field(..., description="Name of the committee")
    committee_code: str = Field(..., description="Committee code/identifier")
    role: str = Field(default="Member", description="Role on committee (Chair, Ranking Member, etc.)")
    start_date: date = Field(..., description="Start date of assignment")
    end_date: Optional[date] = Field(None, description="End date of assignment")
    subcommittees: List[str] = Field(default_factory=list, description="Subcommittee memberships")


class LegislativeAction(BaseModel):
    """Represents a legislative action (vote, sponsorship, etc.)."""
    
    action_id: str = Field(..., description="Unique identifier for the action")
    member_id: str = Field(..., description="Member who took the action")
    action_type: str = Field(..., description="Type of action (vote, sponsor, cosponsor)")
    bill_id: str = Field(..., description="Bill identifier")
    bill_title: str = Field(..., description="Title of the bill")
    action_date: datetime = Field(..., description="Date of the action")
    position: Optional[str] = Field(None, description="Position taken (for votes: Yes/No/Present)")
    industries_affected: List[str] = Field(default_factory=list, description="Industries potentially affected by legislation")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }