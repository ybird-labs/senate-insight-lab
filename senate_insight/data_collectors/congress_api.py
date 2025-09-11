"""Data collector for Congressional information via APIs."""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging

from ..models.congress_member import CongressMember, CommitteeAssignment, LegislativeAction

logger = logging.getLogger(__name__)


class CongressAPICollector:
    """Collects Congressional data from various APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the collector with API credentials."""
        self.api_key = api_key
        self.base_url = "https://api.congress.gov/v3"
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})
    
    def get_current_members(self, chamber: str = "both") -> List[CongressMember]:
        """
        Get current members of Congress.
        
        Args:
            chamber: "senate", "house", or "both"
            
        Returns:
            List of CongressMember objects
        """
        members = []
        
        chambers_to_query = []
        if chamber in ["senate", "both"]:
            chambers_to_query.append("senate")
        if chamber in ["house", "both"]:
            chambers_to_query.append("house")
        
        for chamber_name in chambers_to_query:
            try:
                url = f"{self.base_url}/member/{chamber_name}/117"  # 117th Congress
                response = self.session.get(url, params={"format": "json"})
                response.raise_for_status()
                
                data = response.json()
                
                for member_data in data.get("members", []):
                    member = self._parse_member(member_data, chamber_name)
                    if member:
                        members.append(member)
                        
            except requests.RequestException as e:
                logger.error(f"Error fetching {chamber_name} members: {e}")
        
        return members
    
    def _parse_member(self, data: Dict[str, Any], chamber: str) -> Optional[CongressMember]:
        """Parse member data from API response."""
        try:
            return CongressMember(
                member_id=data.get("bioguideId", ""),
                name=f"{data.get('firstName', '')} {data.get('lastName', '')}".strip(),
                chamber=chamber.title(),
                state=data.get("state", ""),
                district=data.get("district"),
                party=data.get("party", ""),
                start_date=self._parse_date(data.get("startDate")),
                end_date=self._parse_date(data.get("endDate")),
            )
        except Exception as e:
            logger.error(f"Error parsing member data: {e}")
            return None
    
    def get_member_committees(self, member_id: str) -> List[CommitteeAssignment]:
        """Get committee assignments for a member."""
        assignments = []
        
        try:
            url = f"{self.base_url}/member/{member_id}/committee-assignment"
            response = self.session.get(url, params={"format": "json"})
            response.raise_for_status()
            
            data = response.json()
            
            for assignment_data in data.get("committeeAssignments", []):
                assignment = self._parse_committee_assignment(member_id, assignment_data)
                if assignment:
                    assignments.append(assignment)
                    
        except requests.RequestException as e:
            logger.error(f"Error fetching committees for member {member_id}: {e}")
        
        return assignments
    
    def _parse_committee_assignment(self, member_id: str, data: Dict[str, Any]) -> Optional[CommitteeAssignment]:
        """Parse committee assignment data."""
        try:
            return CommitteeAssignment(
                member_id=member_id,
                committee_name=data.get("committeeName", ""),
                committee_code=data.get("committeeCode", ""),
                role=data.get("rank", "Member"),
                start_date=self._parse_date(data.get("startDate")),
                end_date=self._parse_date(data.get("endDate")),
            )
        except Exception as e:
            logger.error(f"Error parsing committee assignment: {e}")
            return None
    
    def get_member_votes(self, member_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[LegislativeAction]:
        """Get voting record for a member."""
        votes = []
        
        try:
            url = f"{self.base_url}/member/{member_id}/vote"
            params = {"format": "json"}
            
            if start_date:
                params["fromDateTime"] = start_date.isoformat()
            if end_date:
                params["toDateTime"] = end_date.isoformat()
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for vote_data in data.get("votes", []):
                vote = self._parse_vote(member_id, vote_data)
                if vote:
                    votes.append(vote)
                    
        except requests.RequestException as e:
            logger.error(f"Error fetching votes for member {member_id}: {e}")
        
        return votes
    
    def _parse_vote(self, member_id: str, data: Dict[str, Any]) -> Optional[LegislativeAction]:
        """Parse vote data."""
        try:
            return LegislativeAction(
                action_id=f"vote_{data.get('voteId', '')}",
                member_id=member_id,
                action_type="vote",
                bill_id=data.get("billNumber", ""),
                bill_title=data.get("billTitle", ""),
                action_date=self._parse_datetime(data.get("voteDate")),
                position=data.get("memberVotePosition", ""),
            )
        except Exception as e:
            logger.error(f"Error parsing vote data: {e}")
            return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
        except Exception:
            return None
    
    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not datetime_str:
            return None
        try:
            return datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        except Exception:
            return None