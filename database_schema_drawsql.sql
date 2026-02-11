-- INQ-ED Database Schema for DrawSQL
-- Educational Platform Database Structure
-- Generated: 2026-02-11

-- ============================================
-- USERS AND AUTHENTICATION
-- ============================================

-- User table (extends Django AbstractUser)
CREATE TABLE "core_user" (
    "id" BIGSERIAL PRIMARY KEY,
    "password" VARCHAR(128) NOT NULL,
    "last_login" TIMESTAMP WITH TIME ZONE,
    "is_superuser" BOOLEAN NOT NULL DEFAULT FALSE,
    "username" VARCHAR(150) UNIQUE NOT NULL,
    "first_name" VARCHAR(150) NOT NULL,
    "last_name" VARCHAR(150) NOT NULL,
    "email" VARCHAR(254) NOT NULL,
    "is_staff" BOOLEAN NOT NULL DEFAULT FALSE,
    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
    "date_joined" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Custom fields
    "role" VARCHAR(20) NOT NULL CHECK (role IN ('teacher', 'student', 'school_admin')),
    "school" VARCHAR(255),
    "bio" TEXT,
    "plain_password" VARCHAR(100),
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "core_user" IS 'Users: Teachers, Students, and School Admins';
COMMENT ON COLUMN "core_user"."role" IS 'User role: teacher, student, or school_admin';
COMMENT ON COLUMN "core_user"."school" IS 'School name for grouping users';
COMMENT ON COLUMN "core_user"."plain_password" IS 'Plain text password for display (students only)';

-- ============================================
-- CLASSES AND ENROLLMENTS
-- ============================================

-- Class table
CREATE TABLE "core_class" (
    "id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "teacher_id" BIGINT NOT NULL,
    "subject" VARCHAR(100) NOT NULL CHECK (subject IN ('english', 'maths', 'english_maths')),
    "year_ks" INTEGER NOT NULL CHECK (year_ks IN (0, 1, 2, 3, 4)),
    "description" TEXT,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("teacher_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_class" IS 'Classes created by teachers';
COMMENT ON COLUMN "core_class"."subject" IS 'english, maths, or english_maths';
COMMENT ON COLUMN "core_class"."year_ks" IS '0=EYFS, 1=KS1, 2=KS2, 3=KS3, 4=KS4';

CREATE INDEX "idx_class_teacher" ON "core_class"("teacher_id");
CREATE INDEX "idx_class_subject" ON "core_class"("subject");
CREATE INDEX "idx_class_year_ks" ON "core_class"("year_ks");

-- ClassStudent table (enrollment junction table)
CREATE TABLE "core_classstudent" (
    "id" BIGSERIAL PRIMARY KEY,
    "student_id" BIGINT NOT NULL,
    "clazz_id" BIGINT NOT NULL,
    "date_joined" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("student_id") REFERENCES "core_user"("id") ON DELETE CASCADE,
    FOREIGN KEY ("clazz_id") REFERENCES "core_class"("id") ON DELETE CASCADE,
    UNIQUE ("student_id", "clazz_id")
);

COMMENT ON TABLE "core_classstudent" IS 'Student enrollments in classes (many-to-many)';

CREATE INDEX "idx_classstudent_student" ON "core_classstudent"("student_id");
CREATE INDEX "idx_classstudent_class" ON "core_classstudent"("clazz_id");

-- ============================================
-- SCHOOL ADMIN
-- ============================================

-- SchoolAnalyticsProfile table
CREATE TABLE "core_schoolanalyticsprofile" (
    "id" BIGSERIAL PRIMARY KEY,
    "teacher_id" BIGINT UNIQUE NOT NULL,
    "school" VARCHAR(255) NOT NULL,
    "can_access_all_teachers" BOOLEAN NOT NULL DEFAULT TRUE,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("teacher_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_schoolanalyticsprofile" IS 'School administrators with cross-teacher access';
COMMENT ON COLUMN "core_schoolanalyticsprofile"."can_access_all_teachers" IS 'Access all teachers data in the same school';

CREATE INDEX "idx_analytics_school" ON "core_schoolanalyticsprofile"("school");

-- ============================================
-- CONTENT AND ANNOUNCEMENTS
-- ============================================

-- NewsAnnouncement table
CREATE TABLE "core_newsannouncement" (
    "id" BIGSERIAL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) UNIQUE NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "excerpt" TEXT,
    "status" VARCHAR(10) NOT NULL CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
    "featured" BOOLEAN NOT NULL DEFAULT FALSE,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "published_at" TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_newsannouncement" IS 'News and announcements (admin only)';
COMMENT ON COLUMN "core_newsannouncement"."featured" IS 'Show on homepage';

CREATE INDEX "idx_news_author" ON "core_newsannouncement"("author_id");
CREATE INDEX "idx_news_status" ON "core_newsannouncement"("status");
CREATE INDEX "idx_news_published" ON "core_newsannouncement"("published_at");

-- HelpTutorial table
CREATE TABLE "core_helptutorial" (
    "id" BIGSERIAL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) UNIQUE NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "excerpt" TEXT,
    "image" VARCHAR(100),
    "status" VARCHAR(10) NOT NULL CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
    "featured" BOOLEAN NOT NULL DEFAULT FALSE,
    "order" INTEGER NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "published_at" TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_helptutorial" IS 'Help guides and tutorials (admin only)';
COMMENT ON COLUMN "core_helptutorial"."order" IS 'Display order (lower numbers first)';

CREATE INDEX "idx_help_author" ON "core_helptutorial"("author_id");
CREATE INDEX "idx_help_status" ON "core_helptutorial"("status");
CREATE INDEX "idx_help_order" ON "core_helptutorial"("order");

-- ============================================
-- TEACHING RESOURCES
-- ============================================

-- TeachingResource table
CREATE TABLE "core_teachingresource" (
    "id" BIGSERIAL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) UNIQUE NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT,
    "excerpt" TEXT,
    "image" VARCHAR(100),
    "file" VARCHAR(100),
    "resource_type" VARCHAR(20) NOT NULL CHECK (resource_type IN ('lesson_plan', 'activity', 'worksheet', 'physical_material', 'game_setup', 'other')) DEFAULT 'other',
    "key_stage" INTEGER,
    "subject" VARCHAR(100),
    "status" VARCHAR(10) NOT NULL CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
    "featured" BOOLEAN NOT NULL DEFAULT FALSE,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "published_at" TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_teachingresource" IS 'Teacher-shared resources (lesson plans, activities, etc.)';
COMMENT ON COLUMN "core_teachingresource"."resource_type" IS 'lesson_plan, activity, worksheet, physical_material, game_setup, other';
COMMENT ON COLUMN "core_teachingresource"."file" IS 'PDF, Word, Excel file upload';

CREATE INDEX "idx_resource_author" ON "core_teachingresource"("author_id");
CREATE INDEX "idx_resource_type" ON "core_teachingresource"("resource_type");
CREATE INDEX "idx_resource_status" ON "core_teachingresource"("status");

-- Resource likes (many-to-many)
CREATE TABLE "core_teachingresource_likes" (
    "id" BIGSERIAL PRIMARY KEY,
    "teachingresource_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    FOREIGN KEY ("teachingresource_id") REFERENCES "core_teachingresource"("id") ON DELETE CASCADE,
    FOREIGN KEY ("user_id") REFERENCES "core_user"("id") ON DELETE CASCADE,
    UNIQUE ("teachingresource_id", "user_id")
);

COMMENT ON TABLE "core_teachingresource_likes" IS 'Teachers who liked resources (many-to-many)';

CREATE INDEX "idx_resource_likes_resource" ON "core_teachingresource_likes"("teachingresource_id");
CREATE INDEX "idx_resource_likes_user" ON "core_teachingresource_likes"("user_id");

-- ResourceComment table
CREATE TABLE "core_resourcecomment" (
    "id" BIGSERIAL PRIMARY KEY,
    "resource_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("resource_id") REFERENCES "core_teachingresource"("id") ON DELETE CASCADE,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_resourcecomment" IS 'Comments on teaching resources';

CREATE INDEX "idx_comment_resource" ON "core_resourcecomment"("resource_id");
CREATE INDEX "idx_comment_author" ON "core_resourcecomment"("author_id");

-- ============================================
-- FORUM
-- ============================================

-- ForumPost table
CREATE TABLE "core_forumpost" (
    "id" BIGSERIAL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "image" VARCHAR(100),
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_pinned" BOOLEAN NOT NULL DEFAULT FALSE,
    "is_locked" BOOLEAN NOT NULL DEFAULT FALSE,
    "views" INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_forumpost" IS 'Teacher community forum posts';
COMMENT ON COLUMN "core_forumpost"."is_pinned" IS 'Pin to top of forum';
COMMENT ON COLUMN "core_forumpost"."is_locked" IS 'Prevent new replies';

CREATE INDEX "idx_forum_author" ON "core_forumpost"("author_id");
CREATE INDEX "idx_forum_pinned" ON "core_forumpost"("is_pinned");

-- ForumReply table
CREATE TABLE "core_forumreply" (
    "id" BIGSERIAL PRIMARY KEY,
    "post_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("post_id") REFERENCES "core_forumpost"("id") ON DELETE CASCADE,
    FOREIGN KEY ("author_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_forumreply" IS 'Replies to forum posts';

CREATE INDEX "idx_reply_post" ON "core_forumreply"("post_id");
CREATE INDEX "idx_reply_author" ON "core_forumreply"("author_id");

-- ============================================
-- AVATARS
-- ============================================

-- Avatar table
CREATE TABLE "core_avatar" (
    "id" BIGSERIAL PRIMARY KEY,
    "user_id" BIGINT UNIQUE NOT NULL,
    "body_type" VARCHAR(20) NOT NULL CHECK (body_type IN ('blob', 'round', 'tall', 'wide', 'pear', 'bean')) DEFAULT 'blob',
    "body_color" VARCHAR(7) NOT NULL DEFAULT '#FF6B9D',
    "eye_type" VARCHAR(20) NOT NULL CHECK (eye_type IN ('big_round', 'small_dots', 'one_eye', 'sleepy', 'googly', 'angry')) DEFAULT 'big_round',
    "mouth_type" VARCHAR(20) NOT NULL CHECK (mouth_type IN ('happy', 'toothy', 'small', 'big_smile', 'oh', 'silly')) DEFAULT 'happy',
    "head_decoration" VARCHAR(20) NOT NULL CHECK (head_decoration IN ('none', 'horns', 'antennae', 'spikes', 'ears', 'mohawk')) DEFAULT 'horns',
    "decoration_color" VARCHAR(7) NOT NULL DEFAULT '#FFB347',
    "pattern" VARCHAR(20) NOT NULL CHECK (pattern IN ('solid', 'spots', 'stripes', 'gradient')) DEFAULT 'solid',
    "pattern_color" VARCHAR(7) NOT NULL DEFAULT '#FF1493',
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "core_user"("id") ON DELETE CASCADE
);

COMMENT ON TABLE "core_avatar" IS 'PixiJS sprite-based monster avatars (ClassDojo-style)';
COMMENT ON COLUMN "core_avatar"."body_color" IS 'Hex color code';
COMMENT ON COLUMN "core_avatar"."decoration_color" IS 'Hex color code';

CREATE INDEX "idx_avatar_user" ON "core_avatar"("user_id");

-- ============================================
-- DJANGO AUTH TABLES (Reference)
-- ============================================
-- Note: Django also creates these tables automatically:
-- - auth_group
-- - auth_group_permissions
-- - auth_permission
-- - core_user_groups
-- - core_user_user_permissions
-- - django_admin_log
-- - django_content_type
-- - django_migrations
-- - django_session
-- - account_emailaddress
-- - account_emailconfirmation
-- - socialaccount_socialaccount
-- - socialaccount_socialapp
-- - socialaccount_socialtoken
