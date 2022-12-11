select_user = """
SELECT * FROM users WHERE user_id = %s
"""

insert_user = """
INSERT INTO users (user_id, full_name) VALUES (%s, %s)  
"""