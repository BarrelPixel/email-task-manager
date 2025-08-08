import openai
import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def extract_tasks(self, subject, body, sender):
        """
        Extract actionable tasks from email content using OpenAI GPT-4
        """
        try:
            # Prepare the prompt for task extraction
            prompt = self._create_task_extraction_prompt(subject, body, sender)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that extracts actionable tasks from emails. You analyze email content and identify specific, actionable items that require follow-up or action."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the response
            tasks = self._parse_ai_response(response.choices[0].message.content)
            
            return tasks
        
        except Exception as e:
            logger.error(f"Failed to extract tasks: {e}")
            return []
    
    def _create_task_extraction_prompt(self, subject, body, sender):
        """
        Create a structured prompt for task extraction
        """
        prompt = f"""
Please analyze the following email and extract any actionable tasks. For each task, provide:
1. A clear, concise description of what needs to be done
2. Priority level (High, Medium, Low) based on urgency indicators and sender importance
3. Category (Follow-up, Meeting Prep, Purchase, General, Review, Approval, Schedule, Research)

Email Details:
- Subject: {subject}
- Sender: {sender}
- Body: {body[:2000]}  # Limit body length to avoid token limits

Guidelines for task extraction:
- Only extract tasks that are clearly actionable
- Consider urgency words like "urgent", "asap", "deadline", "important"
- Consider sender importance (managers, team leads, etc.)
- Look for specific requests, follow-ups, approvals, or action items
- Ignore general information or announcements without clear actions

Return the response as a JSON array of objects with the following structure:
[
    {{
        "description": "Clear description of the task",
        "priority": "High|Medium|Low",
        "category": "Follow-up|Meeting Prep|Purchase|General|Review|Approval|Schedule|Research"
    }}
]

If no actionable tasks are found, return an empty array [].
"""
        return prompt
    
    def _parse_ai_response(self, response_text):
        """
        Parse the AI response and extract tasks
        """
        try:
            # Clean the response text
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            tasks_data = json.loads(response_text)
            
            # Validate and clean tasks
            valid_tasks = []
            for task in tasks_data:
                if isinstance(task, dict) and 'description' in task:
                    # Ensure required fields are present
                    description = task.get('description', '').strip()
                    priority = task.get('priority', 'Medium')
                    category = task.get('category', 'General')
                    
                    # Validate priority
                    if priority not in ['High', 'Medium', 'Low']:
                        priority = 'Medium'
                    
                    # Validate category
                    valid_categories = ['Follow-up', 'Meeting Prep', 'Purchase', 'General', 'Review', 'Approval', 'Schedule', 'Research']
                    if category not in valid_categories:
                        category = 'General'
                    
                    if description:  # Only add tasks with descriptions
                        valid_tasks.append({
                            'description': description,
                            'priority': priority,
                            'category': category
                        })
            
            return valid_tasks
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            return []
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return []
    
    def _determine_priority(self, subject, body, sender):
        """
        Determine priority based on content analysis
        """
        priority_indicators = {
            'high': ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline', 'important'],
            'medium': ['soon', 'this week', 'when possible', 'at your convenience'],
            'low': ['when you have time', 'no rush', 'when convenient']
        }
        
        content = f"{subject} {body}".lower()
        
        # Check for high priority indicators
        for indicator in priority_indicators['high']:
            if indicator in content:
                return 'High'
        
        # Check for medium priority indicators
        for indicator in priority_indicators['medium']:
            if indicator in content:
                return 'Medium'
        
        # Check for low priority indicators
        for indicator in priority_indicators['low']:
            if indicator in content:
                return 'Low'
        
        # Default to medium priority
        return 'Medium'
    
    def _determine_category(self, subject, body):
        """
        Determine category based on content analysis
        """
        content = f"{subject} {body}".lower()
        
        category_keywords = {
            'Follow-up': ['follow up', 'follow-up', 'check in', 'status update', 'response needed'],
            'Meeting Prep': ['meeting', 'agenda', 'prepare', 'presentation', 'discussion'],
            'Purchase': ['purchase', 'buy', 'order', 'invoice', 'payment', 'cost', 'budget'],
            'Review': ['review', 'approve', 'check', 'examine', 'assess'],
            'Approval': ['approve', 'approval', 'authorize', 'sign off', 'permission'],
            'Schedule': ['schedule', 'calendar', 'appointment', 'booking', 'time slot'],
            'Research': ['research', 'investigate', 'look into', 'find out', 'analyze']
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    return category
        
        return 'General'
