from sqlalchemy.orm import Session
from models import WisdomTemplate
from typing import List, Dict, Optional
import json

class WisdomStyleManager:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_styles(self) -> List[Dict]:
        """Get all available wisdom styles with their templates"""
        styles = self.db.query(WisdomTemplate).filter(WisdomTemplate.is_active == True).all()
        
        style_groups = {}
        for style in styles:
            if style.style not in style_groups:
                style_groups[style.style] = {
                    "name": style.style.title(),
                    "templates": []
                }
            
            style_groups[style.style]["templates"].append({
                "id": style.id,
                "name": style.name,
                "template": style.template,
                "variables": json.loads(style.variables) if style.variables else []
            })
        
        return list(style_groups.values())
    
    def get_style_templates(self, style: str) -> List[Dict]:
        """Get templates for a specific style"""
        templates = self.db.query(WisdomTemplate).filter(
            WisdomTemplate.style == style,
            WisdomTemplate.is_active == True
        ).all()
        
        return [
            {
                "id": t.id,
                "name": t.name,
                "template": t.template,
                "variables": json.loads(t.variables) if t.variables else []
            }
            for t in templates
        ]
    
    def create_template(self, name: str, style: str, template: str, variables: List[str], created_by: int) -> Dict:
        """Create a new wisdom template"""
        template_obj = WisdomTemplate(
            name=name,
            style=style,
            template=template,
            variables=json.dumps(variables),
            created_by=created_by
        )
        
        self.db.add(template_obj)
        self.db.commit()
        self.db.refresh(template_obj)
        
        return {
            "id": template_obj.id,
            "name": template_obj.name,
            "style": template_obj.style,
            "template": template_obj.template,
            "variables": variables,
            "created_at": template_obj.created_at.isoformat()
        }
    
    def update_template(self, template_id: int, name: str = None, template: str = None, variables: List[str] = None) -> Dict:
        """Update an existing template"""
        template_obj = self.db.query(WisdomTemplate).filter(WisdomTemplate.id == template_id).first()
        
        if not template_obj:
            raise ValueError("Template not found")
        
        if name:
            template_obj.name = name
        if template:
            template_obj.template = template
        if variables is not None:
            template_obj.variables = json.dumps(variables)
        
        self.db.commit()
        
        return {
            "id": template_obj.id,
            "name": template_obj.name,
            "style": template_obj.style,
            "template": template_obj.template,
            "variables": json.loads(template_obj.variables) if template_obj.variables else []
        }
    
    def delete_template(self, template_id: int) -> bool:
        """Soft delete a template"""
        template_obj = self.db.query(WisdomTemplate).filter(WisdomTemplate.id == template_id).first()
        
        if not template_obj:
            return False
        
        template_obj.is_active = False
        self.db.commit()
        return True
    
    def get_style_examples(self) -> Dict[str, List[str]]:
        """Get example wisdom for each style"""
        return {
            "classic": [
                "The mirror often blames the face it reflects.",
                "Politeness is free; rudeness always collects interest.",
                "A gentle word turns away wrath, but harsh words stir up anger."
            ],
            "stoic": [
                "The best revenge is not to be like your enemy.",
                "You have power over your mind - not outside events.",
                "The obstacle is the way."
            ],
            "zen": [
                "Before enlightenment, chop wood, carry water. After enlightenment, chop wood, carry water.",
                "The moon does not fight. It attacks no one.",
                "If you understand, things are just as they are."
            ],
            "sufi": [
                "The wound is the place where the Light enters you.",
                "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.",
                "What you seek is seeking you."
            ],
            "sarcastic": [
                "The empty vessel makes the loudest sound.",
                "Some people are like clouds. When they disappear, it's a brighter day.",
                "The problem with common sense is that it's not very common."
            ],
            "poetic": [
                "Like a river that flows to the sea, wisdom finds its way to those who listen.",
                "In the garden of discourse, let kindness be the most beautiful flower.",
                "Words are the mirror of the soul; let yours reflect the light."
            ],
            "scientific": [
                "In the laboratory of human interaction, empathy is the most reliable catalyst for change.",
                "Statistical analysis shows that kindness has a 100% success rate in improving relationships.",
                "The laws of physics apply to emotions: every action has an equal and opposite reaction."
            ],
            "humorous": [
                "I'd agree with you, but then we'd both be wrong.",
                "The best way to appreciate your job is to imagine yourself without one.",
                "I'm not arguing, I'm just explaining why I'm right."
            ]
        }
