SELECT DISTINCT video_id
FROM users u, users_classes us, classes_topics ct, video_topics vt, videos v
WHERE u.user_id = us.user_id
AND u.username = "a.smith"
AND ct.class_id = us.class_id
AND vt.topic_id = ct.topic_id
AND vt.video_id = v.video_id
AND v.video_pending is 'false'
ORDER BY date_accepted DESC;

SELECT DISTINCT video_id
FROM users u, users_classes us, classes_topics ct, video_topics vt, videos v
WHERE u.user_id = us.user_id
AND u.username = "a.smith"
AND ct.class_id = us.class_id
AND vt.topic_id = ct.topic_id
AND vt.video_id = v.video_id
AND video_pending is 'true'
ORDER BY date_uploaded DESC;

SELECT DISTINCT video_id, video_title
FROM videos
WHERE video_id IN (    
    SELECT video_id 
    FROM video_topics
    WHERE topic_id IN (   
        SELECT topic_id
        FROM classes_topics
        WHERE class_id IN (
            SELECT class_id
            FROM users_classes
            WHERE user_id IN (
                SELECT user_id
                FROM users
                WHERE username = 'a.smith'))))
AND video_title LIKE '%SQL%'
AND video_pending = 'false'
AND hidden is null or hidden = 'false'
ORDER BY date_uploaded DESC;

SELECT video_id, video_title
FROM videos
WHERE video_id IN (    
    SELECT video_id 
    FROM video_topics
    WHERE topic_id IN (   
        SELECT topic_id
        FROM classes_topics
        WHERE class_id IN (
            SELECT class_id
            FROM users_classes
            WHERE user_id IN (
                SELECT user_id
                FROM users
                WHERE username = 'a.smith'))))
AND video_title LIKE '%%'
AND video_pending = 'false'
AND hidden is null or hidden = 'false'
ORDER BY date_uploaded DESC;

SELECT subject_description, class, topic_description
FROM users u, users_classes us, classes c, classes_topics ct, subjects s,topics t
WHERE u.username = "a.smith"
AND u.user_id = us.user_id
AND us.class_id = c.class_id
AND c.subject_code = s.subject_code
AND c.class_id = ct.class_id
AND ct.topic_id = t.topic_id;

SELECT *
FROM videos
WHERE video_title = 'SQL Tutorial - Full Database Course for Beginners';

INSERT INTO video_topics (video_id, topic_id)
SELECT video_id, topic_id
FROM videos v, topics t
WHERE video_title = 'SQL Tutorial - Full Database Course for Beginners'
AND topic_description = 'Matrices';
