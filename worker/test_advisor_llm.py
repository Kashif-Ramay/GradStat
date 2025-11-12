"""
LLM-powered Test Advisor Assistant
Provides intelligent guidance for statistical test selection
"""

import os
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class TestAdvisorAI:
    """AI assistant for statistical test selection and guidance"""
    
    def __init__(self):
        """Initialize the Test Advisor AI with OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not set - Test Advisor AI features will be disabled")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
            logger.info("Test Advisor AI initialized successfully")
    
    def is_available(self) -> bool:
        """Check if the AI service is available"""
        return self.client is not None
    
    def recommend_from_description(self, description: str, data_summary: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Recommend statistical tests based on user's research description
        
        Args:
            description: User's description of their research scenario
            data_summary: Optional summary of uploaded data
            
        Returns:
            Dictionary with recommendations, reasoning, and alternatives
        """
        if not self.is_available():
            return {
                "error": "AI service not available",
                "message": "Test Advisor AI requires OpenAI API key to be configured"
            }
        
        try:
            # Build context from data summary if available
            data_context = ""
            if data_summary:
                data_context = f"\n\nData Context:\n"
                data_context += f"- Sample size: {data_summary.get('n_rows', 'Unknown')}\n"
                data_context += f"- Variables: {data_summary.get('n_columns', 'Unknown')} columns\n"
                if 'column_types' in data_summary:
                    numeric = sum(1 for t in data_summary['column_types'].values() if t in ['int64', 'float64'])
                    categorical = sum(1 for t in data_summary['column_types'].values() if t == 'object')
                    data_context += f"- Numeric variables: {numeric}\n"
                    data_context += f"- Categorical variables: {categorical}\n"
            
            prompt = f"""You are an expert statistical consultant helping researchers choose the right statistical test.

User's Research Scenario:
{description}
{data_context}

Based on this information, provide:
1. The recommended statistical test(s)
2. Clear reasoning for the recommendation
3. Key assumptions to check
4. Alternative tests if assumptions are violated
5. Sample size considerations

Format your response as a structured recommendation that is clear, practical, and educational.
Focus on the most common and appropriate tests for their scenario.
"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert statistical consultant specializing in helping researchers choose appropriate statistical tests. Provide clear, practical guidance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            recommendation = response.choices[0].message.content
            
            return {
                "recommendation": recommendation,
                "has_data": data_summary is not None,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Recommendation error: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Answer user's question about statistical tests or concepts
        
        Args:
            question: User's question
            context: Optional context (current wizard state, data info)
            
        Returns:
            AI-generated answer
        """
        if not self.is_available():
            return "AI service not available. Please configure OpenAI API key."
        
        try:
            # Build context string
            context_str = ""
            if context:
                if 'current_answers' in context:
                    context_str += f"\n\nCurrent Test Selection Context:\n"
                    for key, value in context['current_answers'].items():
                        context_str += f"- {key}: {value}\n"
                if 'data_summary' in context:
                    context_str += f"\nData: {context['data_summary'].get('n_rows', 'Unknown')} rows, {context['data_summary'].get('n_columns', 'Unknown')} columns\n"
            
            prompt = f"""You are an expert statistical consultant. Answer the following question clearly and concisely.
{context_str}

Question: {question}

Provide a clear, practical answer that helps the user understand the concept and make informed decisions.
Keep the response focused and actionable."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert statistical consultant. Provide clear, concise, and practical answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Question answering error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def explain_assumption(self, assumption_name: str, test_type: Optional[str] = None) -> str:
        """
        Explain a statistical assumption in plain language
        
        Args:
            assumption_name: Name of the assumption (e.g., "normality", "homogeneity of variance")
            test_type: Optional test type for context
            
        Returns:
            Plain-language explanation
        """
        if not self.is_available():
            return "AI service not available. Please configure OpenAI API key."
        
        try:
            test_context = f" for {test_type}" if test_type else ""
            
            prompt = f"""Explain the statistical assumption of "{assumption_name}"{test_context} in simple, practical terms.

Include:
1. What it means in plain language
2. Why it matters
3. How to check if it's met
4. What to do if it's violated

Keep it concise (3-4 sentences) and practical for researchers."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at explaining statistical concepts in simple, practical terms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Assumption explanation error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def compare_tests(self, test1: str, test2: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Compare two statistical tests and explain when to use each
        
        Args:
            test1: First test name
            test2: Second test name
            context: Optional context about the data/scenario
            
        Returns:
            Comparison with pros/cons and recommendation
        """
        if not self.is_available():
            return {
                "error": "AI service not available",
                "message": "Test Advisor AI requires OpenAI API key to be configured"
            }
        
        try:
            context_str = ""
            if context and 'data_summary' in context:
                context_str = f"\n\nUser's Data Context:\n"
                context_str += f"- Sample size: {context['data_summary'].get('n_rows', 'Unknown')}\n"
            
            prompt = f"""Compare these two statistical tests and explain when to use each:

Test 1: {test1}
Test 2: {test2}
{context_str}

Provide:
1. Brief description of each test
2. Key differences
3. Pros and cons of each
4. When to use each test
5. Recommendation for the user's scenario (if context provided)

Format as a clear, structured comparison."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert statistical consultant. Provide clear, practical comparisons of statistical tests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            comparison = response.choices[0].message.content
            
            return {
                "comparison": comparison,
                "test1": test1,
                "test2": test2,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Test comparison error: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    def enhance_auto_detection(self, detection_result: Dict[str, Any], question_type: str) -> str:
        """
        Enhance auto-detection results with AI explanation
        
        Args:
            detection_result: Result from auto-detection
            question_type: Type of question (isNormal, isPaired, etc.)
            
        Returns:
            Enhanced explanation
        """
        if not self.is_available():
            return detection_result.get('explanation', 'Auto-detection complete')
        
        try:
            result_summary = f"Detection: {detection_result.get('answer', 'Unknown')}\n"
            result_summary += f"Confidence: {detection_result.get('confidence', 'Unknown')}\n"
            if 'details' in detection_result:
                result_summary += f"Details: {detection_result['details']}\n"
            
            prompt = f"""Explain this auto-detection result in simple, practical terms:

Question Type: {question_type}
{result_summary}

Provide a brief (2-3 sentences) explanation of:
1. What this means for their analysis
2. Why this matters
3. What they should do next

Be encouraging and practical."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful statistical assistant. Explain auto-detection results clearly and encouragingly."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Enhancement error: {str(e)}")
            return detection_result.get('explanation', 'Auto-detection complete')
    
    def suggest_sample_size(self, test_type: str, current_n: int, effect_size: str = "medium") -> Dict[str, Any]:
        """
        Provide sample size guidance for a given test
        
        Args:
            test_type: Type of statistical test
            current_n: Current sample size
            effect_size: Expected effect size (small/medium/large)
            
        Returns:
            Sample size guidance and power analysis insights
        """
        if not self.is_available():
            return {
                "error": "AI service not available",
                "message": "Test Advisor AI requires OpenAI API key to be configured"
            }
        
        try:
            prompt = f"""Provide sample size guidance for this scenario:

Test Type: {test_type}
Current Sample Size: {current_n}
Expected Effect Size: {effect_size}

Provide:
1. Assessment of current sample size
2. Recommended sample size for adequate power (80%)
3. What they can detect with current sample size
4. Practical advice

Be practical and encouraging. Include specific numbers where possible."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in statistical power analysis. Provide practical sample size guidance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            guidance = response.choices[0].message.content
            
            return {
                "guidance": guidance,
                "current_n": current_n,
                "test_type": test_type,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Sample size guidance error: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
