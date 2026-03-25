"""
Mock Marketing Tools for the Marketing Planning Assistant Agent.

This module provides mock tool implementations for:
- CompetitorResearchTool
- AdDatabaseTool
- BudgetCheckerTool
- MarketTrendTool

Each tool returns realistic mock data for marketing planning tasks.
"""

from typing import Dict, List, Any


class CompetitorResearchTool:
    """Tool for researching competitors in a given market."""
    
    def __init__(self):
        self.name = "CompetitorResearchTool"
        self.description = "Identifies and researches competitors in a specific market segment"
    
    def identify_competitors(self, industry: str, product_type: str) -> List[Dict[str, Any]]:
        """
        Identify top competitors based on industry and product type.
        
        Args:
            industry: The industry sector (e.g., 'technology', 'fashion')
            product_type: The specific product category (e.g., 'smartphone', 'shoes')
            
        Returns:
            List of competitor information dictionaries
        """
        # Mock competitor data
        mock_competitors = {
            "smartphone": [
                {"name": "TechCorp", "market_share": "25%", "key_products": ["Phone X", "Phone Pro"]},
                {"name": "MobileMax", "market_share": "20%", "key_products": ["MaxPhone 12", "MaxPhone Ultra"]},
                {"name": "SmartDevices Inc", "market_share": "15%", "key_products": ["SmartPhone Z", "SmartPhone Lite"]},
                {"name": "GlobalTech", "market_share": "12%", "key_products": ["GT Phone 5", "GT Phone Mini"]},
                {"name": "InnovateMobile", "market_share": "10%", "key_products": ["InnovaPhone A", "InnovaPhone B"]}
            ],
            "fashion": [
                {"name": "StyleCo", "market_share": "18%", "key_products": ["Urban Collection", "Classic Line"]},
                {"name": "TrendSetters", "market_share": "15%", "key_products": ["Seasonal Wear", "Accessories"]},
                {"name": "FashionForward", "market_share": "12%", "key_products": ["Designer Series", "Casual Wear"]}
            ]
        }
        
        return mock_competitors.get(product_type.lower(), [
            {"name": "Generic Competitor 1", "market_share": "20%", "key_products": ["Product A"]},
            {"name": "Generic Competitor 2", "market_share": "15%", "key_products": ["Product B"]},
            {"name": "Generic Competitor 3", "market_share": "10%", "key_products": ["Product C"]}
        ])
    
    def get_competitor_strategies(self, competitor_name: str) -> Dict[str, Any]:
        """
        Get detailed strategy information for a specific competitor.
        
        Args:
            competitor_name: Name of the competitor
            
        Returns:
            Dictionary containing competitor strategy details
        """
        return {
            "competitor": competitor_name,
            "pricing_strategy": "Premium pricing with seasonal discounts",
            "target_audience": "Tech-savvy professionals aged 25-45",
            "marketing_channels": ["Social Media", "TV Ads", "Influencer Partnerships"],
            "unique_selling_points": ["Advanced AI features", "Premium build quality", "Ecosystem integration"]
        }


class AdDatabaseTool:
    """Tool for accessing and analyzing advertisement databases."""
    
    def __init__(self):
        self.name = "AdDatabaseTool"
        self.description = "Accesses database of advertisements for analysis"
    
    def collect_ads(self, competitor_name: str, platform: str = "all") -> List[Dict[str, Any]]:
        """
        Collect advertisements from a specific competitor.
        
        Args:
            competitor_name: Name of the competitor
            platform: Platform filter (e.g., 'facebook', 'google', 'tv', 'all')
            
        Returns:
            List of advertisement data dictionaries
        """
        # Mock ad data
        mock_ads = [
            {
                "id": "AD001",
                "competitor": competitor_name,
                "platform": "facebook",
                "content": "Introducing the future of mobile technology. Experience innovation like never before.",
                "visual_theme": "Sleek, modern design with blue accents",
                "call_to_action": "Pre-order now",
                "engagement_metrics": {"likes": 15000, "shares": 3200, "comments": 890}
            },
            {
                "id": "AD002",
                "competitor": competitor_name,
                "platform": "instagram",
                "content": "Capture life's moments in stunning detail. #Photography #Innovation",
                "visual_theme": "Lifestyle photography with vibrant colors",
                "call_to_action": "Learn more",
                "engagement_metrics": {"likes": 22000, "shares": 4500, "comments": 1200}
            },
            {
                "id": "AD003",
                "competitor": competitor_name,
                "platform": "youtube",
                "content": "Watch our latest product demo featuring groundbreaking AI capabilities",
                "visual_theme": "Professional video production with demonstrations",
                "call_to_action": "Subscribe and visit our website",
                "engagement_metrics": {"views": 500000, "likes": 35000, "comments": 2800}
            },
            {
                "id": "AD004",
                "competitor": competitor_name,
                "platform": "tv",
                "content": "30-second spot highlighting premium features and lifestyle benefits",
                "visual_theme": "High-production value with celebrity endorsement",
                "call_to_action": "Available at retailers nationwide",
                "engagement_metrics": {"estimated_reach": "2M viewers"}
            }
        ]
        
        if platform.lower() == "all":
            return mock_ads
        
        return [ad for ad in mock_ads if ad["platform"].lower() == platform.lower()]
    
    def analyze_ad_messaging(self, ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the messaging themes across multiple advertisements.
        
        Args:
            ads: List of advertisement dictionaries
            
        Returns:
            Analysis results including themes, tone, and key messages
        """
        return {
            "total_ads_analyzed": len(ads),
            "common_themes": [
                "Innovation and technology advancement",
                "Premium quality and craftsmanship",
                "User experience and convenience",
                "Lifestyle enhancement"
            ],
            "tone_analysis": {
                "primary_tone": "Aspirational",
                "secondary_tone": "Professional",
                "emotional_appeal": "High"
            },
            "key_messages": [
                "Cutting-edge technology",
                "Superior performance",
                "Seamless integration into daily life",
                "Status symbol"
            ],
            "visual_patterns": [
                "Minimalist design aesthetics",
                "Focus on product features",
                "Lifestyle integration scenarios"
            ]
        }


class BudgetCheckerTool:
    """Tool for checking and validating marketing budgets."""
    
    def __init__(self):
        self.name = "BudgetCheckerTool"
        self.description = "Validates budget availability for marketing activities"
    
    def check_budget_availability(self, total_budget: float, currency: str = "USD") -> Dict[str, Any]:
        """
        Check overall budget availability and allocation recommendations.
        
        Args:
            total_budget: Total marketing budget amount
            currency: Currency code (default: USD)
            
        Returns:
            Budget availability status and recommendations
        """
        # Mock budget allocation
        recommended_allocation = {
            "digital_advertising": 0.35,
            "content_creation": 0.20,
            "influencer_partnerships": 0.15,
            "traditional_media": 0.15,
            "events_and_sponsorships": 0.10,
            "analytics_and_tools": 0.05
        }
        
        return {
            "total_budget": f"{currency} {total_budget:,.2f}",
            "status": "Available",
            "recommended_allocation": {
                category: f"{currency} {amount * total_budget:,.2f}" 
                for category, amount in recommended_allocation.items()
            },
            "allocation_percentages": recommended_allocation,
            "budget_utilization_forecast": "Optimal",
            "roi_expectation": "15-25% increase in brand awareness"
        }
    
    def validate_task_budget(self, task_name: str, estimated_cost: float) -> Dict[str, Any]:
        """
        Validate budget for a specific marketing task.
        
        Args:
            task_name: Name of the marketing task
            estimated_cost: Estimated cost for the task
            
        Returns:
            Validation result and recommendations
        """
        # Mock validation logic
        budget_ranges = {
            "competitor_research": (500, 5000),
            "ad_collection": (1000, 10000),
            "messaging_analysis": (2000, 15000),
            "trend_identification": (1500, 8000),
            "strategy_generation": (3000, 20000)
        }
        
        task_key = task_name.lower().replace(" ", "_")
        min_budget, max_budget = budget_ranges.get(task_key, (1000, 10000))
        
        is_valid = min_budget <= estimated_cost <= max_budget
        
        return {
            "task": task_name,
            "estimated_cost": f"${estimated_cost:,.2f}",
            "recommended_range": f"${min_budget:,.2f} - ${max_budget:,.2f}",
            "status": "Within Range" if is_valid else "Review Recommended",
            "validation_passed": is_valid,
            "recommendation": "Budget approved for execution" if is_valid else "Consider adjusting budget allocation"
        }


class MarketTrendTool:
    """Tool for identifying and analyzing market trends."""
    
    def __init__(self):
        self.name = "MarketTrendTool"
        self.description = "Analyzes current market trends and patterns"
    
    def identify_trends(self, industry: str, time_period: str = "current_quarter") -> Dict[str, Any]:
        """
        Identify current and emerging trends in a specific industry.
        
        Args:
            industry: Industry sector to analyze
            time_period: Time period for trend analysis
            
        Returns:
            Dictionary containing identified trends and insights
        """
        # Mock trend data
        mock_trends = {
            "technology": {
                "trending_topics": [
                    "AI-powered features",
                    "Sustainability and eco-friendly materials",
                    "5G connectivity",
                    "Foldable displays",
                    "Privacy-focused design"
                ],
                "consumer_preferences": [
                    "Longer battery life",
                    "Better camera quality",
                    "Seamless ecosystem integration",
                    "Affordable premium options"
                ],
                "emerging_technologies": [
                    "Augmented Reality (AR)",
                    "Machine Learning optimization",
                    "Biometric authentication",
                    "Wireless charging advancements"
                ],
                "market_growth_areas": [
                    "Mid-range premium segment",
                    "Accessory ecosystem",
                    "Software services subscription"
                ]
            },
            "fashion": {
                "trending_topics": [
                    "Sustainable fashion",
                    "Athleisure wear",
                    "Vintage revival",
                    "Gender-neutral clothing",
                    "Digital fashion shows"
                ],
                "consumer_preferences": [
                    "Comfort-focused designs",
                    "Versatile pieces",
                    "Ethical production",
                    "Online shopping experience"
                ],
                "emerging_technologies": [
                    "Virtual try-on",
                    "AI-powered styling",
                    "3D printing",
                    "Blockchain for authenticity"
                ],
                "market_growth_areas": [
                    "Direct-to-consumer brands",
                    "Rental and resale markets",
                    "Personalized customization"
                ]
            }
        }
        
        default_trends = {
            "trending_topics": ["Digital transformation", "Customer experience focus", "Sustainability"],
            "consumer_preferences": ["Value for money", "Quality over quantity", "Brand authenticity"],
            "emerging_technologies": ["AI and automation", "Data analytics", "Cloud solutions"],
            "market_growth_areas": ["Online channels", "Subscription models", "Personalization"]
        }
        
        return mock_trends.get(industry.lower(), default_trends)
    
    def analyze_competitor_trends(self, competitors: List[str]) -> Dict[str, Any]:
        """
        Analyze trends across competitor strategies.
        
        Args:
            competitors: List of competitor names
            
        Returns:
            Analysis of common trends among competitors
        """
        return {
            "competitors_analyzed": len(competitors),
            "common_strategies": [
                "Increased digital advertising spend",
                "Focus on social media engagement",
                "Influencer partnership programs",
                "Content marketing initiatives",
                "Customer loyalty programs"
            ],
            "differentiation_opportunities": [
                "Niche market targeting",
                "Unique value proposition emphasis",
                "Innovative channel selection",
                "Community building initiatives"
            ],
            "trend_adoption_rate": {
                "early_adopters": ["TechCorp", "InnovateMobile"],
                "mainstream": ["MobileMax", "SmartDevices Inc"],
                "laggards": ["GlobalTech"]
            }
        }


# Tool registry for easy access
MARKETING_TOOLS = {
    "CompetitorResearchTool": CompetitorResearchTool,
    "AdDatabaseTool": AdDatabaseTool,
    "BudgetCheckerTool": BudgetCheckerTool,
    "MarketTrendTool": MarketTrendTool
}


def get_available_tools() -> List[str]:
    """Return list of available marketing tools."""
    return list(MARKETING_TOOLS.keys())


def initialize_all_tools() -> Dict[str, Any]:
    """Initialize all marketing tools and return them as a dictionary."""
    return {
        "competitor_research": CompetitorResearchTool(),
        "ad_database": AdDatabaseTool(),
        "budget_checker": BudgetCheckerTool(),
        "market_trend": MarketTrendTool()
    }
