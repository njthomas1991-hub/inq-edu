# INQ-ED Database Schema Documentation

## Overview
Educational platform database with 11 core tables supporting teachers, students, school admins, classes, resources, and community features.

---

## Core Tables & Relationships

### 1. **core_user** (Central Users Table)
**Purpose:** All users (Teachers, Students, School Admins)

**Key Fields:**
- `id` (PK)
- `username`, `email`, `password`
- `role` ('teacher', 'student', 'school_admin')
- `school` (for grouping by institution)
- `plain_password` (students only - for teacher reference)

**Relationships:**
- **1:Many** → `core_class` (teacher creates classes)
- **Many:Many** → `core_class` (via `core_classstudent`)
- **1:1** → `core_schoolanalyticsprofile` (school admin profile)
- **1:1** → `core_avatar` (user avatar)
- **1:Many** → `core_teachingresource`, `core_forumpost`, etc. (content authorship)

---

### 2. **core_class** (Classes/Courses)
**Purpose:** Classes created by teachers

**Key Fields:**
- `id` (PK)
- `name` (class name)
- `teacher_id` (FK → core_user)
- `subject` ('english', 'maths', 'english_maths')
- `year_ks` (0=EYFS, 1=KS1, 2=KS2, 3=KS3, 4=KS4)
- `description`

**Relationships:**
- **Many:1** → `core_user` (teacher who created it)
- **Many:Many** → `core_user` (via `core_classstudent` - enrolled students)

---

### 3. **core_classstudent** (Enrollment Junction Table)
**Purpose:** Links students to classes (Many-to-Many)

**Key Fields:**
- `id` (PK)
- `student_id` (FK → core_user)
- `clazz_id` (FK → core_class)
- `date_joined`

**Constraints:**
- UNIQUE (`student_id`, `clazz_id`)

**Relationships:**
- **Many:1** → `core_user` (student)
- **Many:1** → `core_class` (class)

---

### 4. **core_schoolanalyticsprofile** (School Admins)
**Purpose:** School administrators with cross-teacher access

**Key Fields:**
- `id` (PK)
- `teacher_id` (FK → core_user, UNIQUE)
- `school` (school name)
- `can_access_all_teachers` (boolean)

**Relationships:**
- **1:1** → `core_user` (school admin user)

**Note:** School admins can view all teachers/classes/students in their school

---

### 5. **core_newsannouncement** (News & Announcements)
**Purpose:** Admin-created news posts

**Key Fields:**
- `id` (PK)
- `title`, `slug`, `content`, `excerpt`
- `author_id` (FK → core_user)
- `status` ('draft', 'published')
- `featured` (show on homepage)

**Relationships:**
- **Many:1** → `core_user` (author)

---

### 6. **core_helptutorial** (Help Guides)
**Purpose:** Admin-created help documentation

**Key Fields:**
- `id` (PK)
- `title`, `slug`, `content`, `excerpt`
- `author_id` (FK → core_user)
- `status` ('draft', 'published')
- `order` (display sequence)
- `image` (file path)

**Relationships:**
- **Many:1** → `core_user` (author)

---

### 7. **core_teachingresource** (Teacher Resources)
**Purpose:** Teacher-shared lesson plans, worksheets, activities

**Key Fields:**
- `id` (PK)
- `title`, `slug`, `content`, `excerpt`
- `author_id` (FK → core_user)
- `resource_type` ('lesson_plan', 'activity', 'worksheet', 'physical_material', 'game_setup', 'other')
- `key_stage` (1-4)
- `subject`
- `image`, `file` (uploads)
- `status` ('draft', 'published')

**Relationships:**
- **Many:1** → `core_user` (author)
- **Many:Many** → `core_user` (via `core_teachingresource_likes` - teachers who liked)
- **1:Many** → `core_resourcecomment` (comments)

---

### 8. **core_teachingresource_likes** (Resource Likes Junction)
**Purpose:** Tracks which teachers liked which resources

**Key Fields:**
- `id` (PK)
- `teachingresource_id` (FK → core_teachingresource)
- `user_id` (FK → core_user)

**Constraints:**
- UNIQUE (`teachingresource_id`, `user_id`)

---

### 9. **core_resourcecomment** (Resource Comments)
**Purpose:** Comments on teaching resources

**Key Fields:**
- `id` (PK)
- `resource_id` (FK → core_teachingresource)
- `author_id` (FK → core_user)
- `content`

**Relationships:**
- **Many:1** → `core_teachingresource` (parent resource)
- **Many:1** → `core_user` (comment author)

---

### 10. **core_forumpost** (Forum Posts)
**Purpose:** Teacher community discussion threads

**Key Fields:**
- `id` (PK)
- `title`, `content`
- `author_id` (FK → core_user)
- `image` (optional)
- `is_pinned`, `is_locked`
- `views`

**Relationships:**
- **Many:1** → `core_user` (author)
- **1:Many** → `core_forumreply` (replies)

---

### 11. **core_forumreply** (Forum Replies)
**Purpose:** Replies to forum posts

**Key Fields:**
- `id` (PK)
- `post_id` (FK → core_forumpost)
- `author_id` (FK → core_user)
- `content`

**Relationships:**
- **Many:1** → `core_forumpost` (parent post)
- **Many:1** → `core_user` (reply author)

---

### 12. **core_avatar** (User Avatars)
**Purpose:** PixiJS sprite-based monster avatars (ClassDojo-style)

**Key Fields:**
- `id` (PK)
- `user_id` (FK → core_user, UNIQUE)
- `body_type` ('blob', 'round', 'tall', 'wide', 'pear', 'bean')
- `body_color` (hex color)
- `eye_type`, `mouth_type`, `head_decoration`
- `pattern`, `pattern_color`

**Relationships:**
- **1:1** → `core_user` (avatar owner)

---

## Key Relationship Summary

```
core_user (Users)
├─[1:M]─> core_class (as teacher)
├─[M:M]─> core_class (as student, via core_classstudent)
├─[1:1]─> core_schoolanalyticsprofile (school admin)
├─[1:1]─> core_avatar
├─[1:M]─> core_newsannouncement (as author)
├─[1:M]─> core_helptutorial (as author)
├─[1:M]─> core_teachingresource (as author)
├─[M:M]─> core_teachingresource (likes, via core_teachingresource_likes)
├─[1:M]─> core_resourcecomment (as author)
├─[1:M]─> core_forumpost (as author)
└─[1:M]─> core_forumreply (as author)

core_class (Classes)
├─[M:1]─> core_user (teacher)
└─[M:M]─> core_user (students, via core_classstudent)

core_teachingresource (Resources)
├─[M:1]─> core_user (author)
├─[M:M]─> core_user (likes, via core_teachingresource_likes)
└─[1:M]─> core_resourcecomment (comments)

core_forumpost (Forum Posts)
├─[M:1]─> core_user (author)
└─[1:M]─> core_forumreply (replies)
```

---

## Import Instructions for DrawSQL

1. Go to https://drawsql.app/
2. Click "New Diagram"
3. Click "Import" → "From SQL"
4. Paste contents of `database_schema_drawsql.sql`
5. DrawSQL will auto-generate the visual diagram with relationships

**Alternative:** Use the "PostgreSQL" dialect when importing

---

## Index Strategy

**Performance Indexes:**
- All foreign keys have indexes
- `core_user.role` and `core_user.school` for filtering
- `core_class.subject` and `core_class.year_ks` for analytics
- `core_*.(status, published_at)` for content queries
- `core_forumpost.is_pinned` for forum display

---

## Data Integrity Rules

1. **User Roles:** Enforced via CHECK constraints ('teacher', 'student', 'school_admin')
2. **Subject Choices:** Enforced via CHECK ('english', 'maths', 'english_maths')
3. **Key Stages:** Enforced via CHECK (0, 1, 2, 3, 4)
4. **Unique Enrollments:** `core_classstudent` has UNIQUE constraint on (student_id, clazz_id)
5. **Unique Likes:** `core_teachingresource_likes` has UNIQUE constraint on (resource_id, user_id)
6. **Cascading Deletes:** All foreign keys use ON DELETE CASCADE

---

## Analytics Queries

**School Admin Scope:**
```sql
-- All teachers in a school
SELECT * FROM core_user 
WHERE role = 'teacher' AND school = 'School Name';

-- All classes in a school
SELECT c.* FROM core_class c
JOIN core_user u ON c.teacher_id = u.id
WHERE u.school = 'School Name';

-- All students in a school
SELECT DISTINCT u.* FROM core_user u
JOIN core_classstudent cs ON u.id = cs.student_id
JOIN core_class c ON cs.clazz_id = c.id
JOIN core_user t ON c.teacher_id = t.id
WHERE t.school = 'School Name';
```

**Teacher Analytics:**
```sql
-- Classes by subject
SELECT subject, COUNT(*) FROM core_class
WHERE teacher_id = 123
GROUP BY subject;

-- Students across all classes
SELECT COUNT(DISTINCT student_id) FROM core_classstudent
WHERE clazz_id IN (SELECT id FROM core_class WHERE teacher_id = 123);
```
