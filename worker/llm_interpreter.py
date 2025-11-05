"""
LLM-powered statistical interpretation service
Uses OpenAI GPT to explain results and answer questions
"""

import os
import json
from typing import Dict, Any, List, Optional
import logging

# Try to import openai, but don't fail if not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

logger = logging.getLogger(__name__)


class StatisticalInterpreter:
    """
    AI-powered statistical interpreter using OpenAI GPT
    Provides plain-language explanations, answers questions, and explores scenarios
    """
    
    def __init__(self):
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI package not installed - LLM features will be disabled")
            self.api_key = None
            self.model = None
            return
            
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - LLM features will be disabled")
        else:
            openai.api_key = self.api_key
        self.model = "gpt-4o-mini"  # Cost-effective model
        
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return OPENAI_AVAILABLE and self.api_key is not None
    
    def create_context_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """
        Create a comprehensive context prompt from analysis results
        """
        analysis_type = analysis_data.get('analysis_type', 'Unknown')
        sample_size = analysis_data.get('sample_size', 'N/A')
        variables = analysis_data.get('variables', [])
        results = analysis_data.get('results', {})
        assumptions = analysis_data.get('assumptions', {})
        
        prompt = f"""You are a statistical analysis expert helping graduate students understand their research results.

**Analysis Type:** {analysis_type}

**Dataset Information:**
- Sample size: {sample_size}
- Variables: {', '.join(variables) if variables else 'Not specified'}

**Statistical Results:**
{json.dumps(results, indent=2)}

**Assumptions Checked:**
{json.dumps(assumptions, indent=2)}

Your role is to:
1. Explain what these results mean in plain language
2. Highlight important findings
3. Point out any concerns or limitations
4. Suggest next steps
5. Answer follow-up questions about the analysis

Be clear, accurate, and educational. Use analogies when helpful. Avoid jargon unless explaining it.
"""
        return prompt
    
    def interpret_results(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate initial interpretation of results
        
        Args:
            analysis_data: Dictionary containing analysis results and metadata
            
        Returns:
            Dictionary with interpretation, key findings, concerns, and next steps
        """
        if not self.is_available():
            return {
                "error": "LLM service not available. Please set OPENAI_API_KEY.",
                "interpretation": "AI interpretation is currently unavailable.",
                "key_findings": [],
                "concerns": [],
                "next_steps": []
            }
        
        try:
            context = self.create_context_prompt(analysis_data)
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert statistician and educator who explains complex statistical concepts in simple terms."},
                    {"role": "user", "content": context + "\n\nProvide a comprehensive interpretation of these results in 3-4 paragraphs."}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            interpretation = response.choices[0].message.content
            
            return {
                "interpretation": interpretation,
                "key_findings": self._extract_key_findings(analysis_data),
                "concerns": self._identify_concerns(analysis_data),
                "next_steps": self._suggest_next_steps(analysis_data)
            }
        except Exception as e:
            logger.error(f"Interpretation error: {str(e)}")
            return {
                "error": str(e),
                "interpretation": "Failed to generate interpretation. Please try again.",
                "key_findings": self._extract_key_findings(analysis_data),
                "concerns": self._identify_concerns(analysis_data),
                "next_steps": self._suggest_next_steps(analysis_data)
            }
    
    def answer_question(
        self, 
        question: str, 
        analysis_data: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Answer a specific question about the analysis
        
        Args:
            question: User's question
            analysis_data: Analysis results and metadata
            conversation_history: Previous conversation messages
            
        Returns:
            AI-generated answer
        """
        if not self.is_available():
            return "AI question answering is currently unavailable. Please set OPENAI_API_KEY."
        
        try:
            context = self.create_context_prompt(analysis_data)
            
            messages = [
                {"role": "system", "content": "You are an expert statistician answering questions about research results. Be concise but thorough."},
                {"role": "user", "content": context}
            ]
            
            # Add conversation history if exists
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 3 exchanges
            
            # Add current question
            messages.append({"role": "user", "content": question})
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Question answering error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def what_if_analysis(
        self, 
        scenario: str, 
        analysis_data: Dict[str, Any]
    ) -> str:
        """
        Answer "what if" questions about the analysis
        
        Args:
            scenario: Hypothetical scenario to explore
            analysis_data: Analysis results and metadata
            
        Returns:
            AI-generated scenario analysis
        """
        if not self.is_available():
            return "AI scenario analysis is currently unavailable. Please set OPENAI_API_KEY."
        
        try:
            context = self.create_context_prompt(analysis_data)
            
            prompt = f"""Based on the analysis results above, answer this "what if" question:

{scenario}

Consider:
- Current sample size and statistical power
- Effect sizes observed
- Statistical assumptions
- Practical significance
- Methodological implications

Provide a thoughtful, evidence-based response in 2-3 paragraphs."""
            
            messages = [
                {"role": "system", "content": "You are an expert statistician exploring hypothetical scenarios based on research data."},
                {"role": "user", "content": context},
                {"role": "user", "content": prompt}
            ]
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,  # Slightly more creative for scenarios
                max_tokens=600
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"What-if analysis error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _extract_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Extract key statistical findings from results"""
        findings = []
        results = data.get('results', {})
        
        # Check for p-value
        if 'p_value' in results:
            p = float(results['p_value']) if isinstance(results['p_value'], str) else results['p_value']
            if p < 0.001:
                findings.append(f"Highly significant result (p < 0.001)")
            elif p < 0.05:
                findings.append(f"Statistically significant result (p = {p:.4f})")
            else:
                findings.append(f"Not statistically significant (p = {p:.4f})")
        
        # Check effect size
        if 'effect_size' in results:
            effect = results['effect_size']
            if isinstance(effect, dict):
                effect_val = float(effect.get('value', 0)) if isinstance(effect.get('value', 0), str) else effect.get('value', 0)
                effect_type = effect.get('type', 'Effect size')
                findings.append(f"{effect_type}: {effect_val:.3f}")
            else:
                effect_num = float(effect) if isinstance(effect, str) else effect
                findings.append(f"Effect size: {effect_num:.3f}")
        
        # Check R-squared for regression
        if 'r_squared' in results:
            r2 = float(results['r_squared']) if isinstance(results['r_squared'], str) else results['r_squared']
            findings.append(f"Model explains {r2*100:.1f}% of variance (R² = {r2:.3f})")
        
        # Check AUC for classification
        if 'auc' in results:
            auc = float(results['auc']) if isinstance(results['auc'], str) else results['auc']
            if auc > 0.9:
                findings.append(f"Excellent classification performance (AUC = {auc:.3f})")
            elif auc > 0.8:
                findings.append(f"Good classification performance (AUC = {auc:.3f})")
            else:
                findings.append(f"Moderate classification performance (AUC = {auc:.3f})")
        
        return findings if findings else ["Results available for interpretation"]
    
    def _identify_concerns(self, data: Dict[str, Any]) -> List[str]:
        """Identify potential concerns in the analysis"""
        concerns = []
        
        # Small sample size
        sample_size = data.get('sample_size', 0)
        if sample_size < 30:
            concerns.append(f"Small sample size (n = {sample_size}) may limit generalizability")
        
        # Assumption violations
        assumptions = data.get('assumptions', {})
        for assumption, result in assumptions.items():
            if isinstance(result, dict):
                passed = result.get('passed', True)
                if not passed:
                    concerns.append(f"Violated assumption: {assumption}")
        
        # Low power
        results = data.get('results', {})
        if 'power' in results:
            power = float(results['power']) if isinstance(results['power'], str) else results['power']
            if power < 0.8:
                concerns.append(f"Low statistical power ({power:.2f}) - risk of Type II error")
        
        # High p-value with small sample
        if 'p_value' in results and results['p_value'] > 0.05 and sample_size < 50:
            concerns.append("Non-significant result with small sample - may need more data")
        
        return concerns
    
    def _suggest_next_steps(self, data: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on results"""
        steps = []
        results = data.get('results', {})
        sample_size = data.get('sample_size', 0)
        
        # Based on significance
        if 'p_value' in results:
            if results['p_value'] < 0.05:
                steps.append("✓ Consider replication with independent sample")
                steps.append("✓ Explore practical significance and real-world impact")
                steps.append("✓ Examine effect sizes and confidence intervals")
            else:
                steps.append("→ Consider increasing sample size for more power")
                steps.append("→ Explore alternative analyses or transformations")
                steps.append("→ Check for potential confounding variables")
        
        # Based on sample size
        if sample_size < 100:
            steps.append("→ Larger sample would strengthen conclusions")
        
        # Based on assumptions
        assumptions = data.get('assumptions', {})
        violated = [k for k, v in assumptions.items() if isinstance(v, dict) and not v.get('passed', True)]
        if violated:
            steps.append(f"→ Address assumption violations: {', '.join(violated)}")
        
        return steps if steps else ["Review results and consider research implications"]
