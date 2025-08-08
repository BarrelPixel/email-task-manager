#!/usr/bin/env python3
"""
Database migration script to add indexes for better performance
"""
from extensions import db
from run import create_app
from sqlalchemy import text

def create_indexes():
    """Create database indexes for better performance"""
    
    indexes_to_create = [
        # User table indexes
        "CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);",
        
        # Task table indexes
        "CREATE INDEX IF NOT EXISTS idx_task_user_id ON tasks(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_task_email_id ON tasks(email_id);",
        "CREATE INDEX IF NOT EXISTS idx_task_sender ON tasks(sender);",
        "CREATE INDEX IF NOT EXISTS idx_task_priority ON tasks(priority);",
        "CREATE INDEX IF NOT EXISTS idx_task_category ON tasks(category);",
        "CREATE INDEX IF NOT EXISTS idx_task_completed ON tasks(completed);",
        "CREATE INDEX IF NOT EXISTS idx_task_completed_at ON tasks(completed_at);",
        "CREATE INDEX IF NOT EXISTS idx_task_created_at ON tasks(created_at);",
        
        # Email table indexes
        "CREATE INDEX IF NOT EXISTS idx_email_user_id ON emails(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_email_gmail_id ON emails(gmail_id);",
        "CREATE INDEX IF NOT EXISTS idx_email_thread_id ON emails(thread_id);",
        "CREATE INDEX IF NOT EXISTS idx_email_sender ON emails(sender);",
        "CREATE INDEX IF NOT EXISTS idx_email_sender_email ON emails(sender_email);",
        "CREATE INDEX IF NOT EXISTS idx_email_processed ON emails(processed);",
        "CREATE INDEX IF NOT EXISTS idx_email_processed_at ON emails(processed_at);",
        "CREATE INDEX IF NOT EXISTS idx_email_received_at ON emails(received_at);",
        "CREATE INDEX IF NOT EXISTS idx_email_created_at ON emails(created_at);",
        
        # Composite indexes for common queries
        "CREATE INDEX IF NOT EXISTS idx_task_user_completed ON tasks(user_id, completed);",
        "CREATE INDEX IF NOT EXISTS idx_task_user_priority_completed ON tasks(user_id, priority, completed);",
        "CREATE INDEX IF NOT EXISTS idx_task_user_category_completed ON tasks(user_id, category, completed);",
        "CREATE INDEX IF NOT EXISTS idx_email_user_processed ON emails(user_id, processed);",
    ]
    
    with create_app().app_context():
        for index_sql in indexes_to_create:
            try:
                db.session.execute(text(index_sql))
                print(f"[OK] Created: {index_sql}")
            except Exception as e:
                print(f"[FAIL] Failed: {index_sql} - {e}")
        
        try:
            db.session.commit()
            print("\n[SUCCESS] All database indexes created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Failed to commit indexes: {e}")

if __name__ == '__main__':
    create_indexes()