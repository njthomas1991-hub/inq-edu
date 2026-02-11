# GitHub Projects Setup Guide

This document contains all user stories and setup instructions for GitHub Projects board.

---

## Quick Setup Instructions

1. Go to your GitHub repository: https://github.com/njthomas1991-hub/inq-edu
2. Click **Projects** tab → **New Project**
3. Select **Board** template
4. Name it: "INQ-ED Development Board"
5. Create columns: **Backlog**, **In Progress**, **Done**, **Testing**
6. Add the user stories below as issues
7. Link issues to commits as you work

---

## User Stories

### Epic 1: Authentication & User Management

#### US-1.1: User Registration
**As a** teacher  
**I want to** register for an account with my school details  
**So that** I can access the platform and create classes

**Acceptance Criteria:**
- Registration form includes: username, email, password, full name, school, role
- Email validation is enforced
- Password strength requirements met
- User redirected to teacher dashboard after signup

**Priority:** HIGH  
**Story Points:** 5

---

#### US-1.2: Role-Based Login
**As a** user (teacher/student/school_admin)  
**I want to** log in and be redirected to my role-specific dashboard  
**So that** I see content relevant to my role

**Acceptance Criteria:**
- Teachers → `/teacher/` dashboard
- Students → `/student/` dashboard  
- School Admins → `/school-admin/` dashboard
- Invalid credentials show error message
- "Forgot password" link available

**Priority:** HIGH  
**Story Points:** 3

---

#### US-1.3: Student Account Creation
**As a** teacher  
**I want to** create student accounts directly from my dashboard  
**So that** students can access the platform without manual registration

**Acceptance Criteria:**
- Form includes: username, full name, year/key stage
- Auto-generated passwords are secure and user-friendly
- Student immediately added to teacher's class
- Credentials displayed for teacher to share

**Priority:** HIGH  
**Story Points:** 5

---

### Epic 2: Class Management

#### US-2.1: Create Class
**As a** teacher  
**I want to** create a new class with subject and year group  
**So that** I can organize my students by teaching groups

**Acceptance Criteria:**
- Form includes: class name, subject (dropdown), year/key stage (dropdown), description
- Class appears on teacher dashboard immediately
- Unique class code generated for identification
- Validation prevents duplicate class names

**Priority:** HIGH  
**Story Points:** 3

---

#### US-2.2: View Class Details
**As a** teacher  
**I want to** view all students enrolled in a specific class  
**So that** I can see class composition and student information

**Acceptance Criteria:**
- Student list displays: name, username, avatar, join date
- Total student count shown
- Link to add new students visible
- Option to remove students from class

**Priority:** MEDIUM  
**Story Points:** 3

---

#### US-2.3: Add Student to Class
**As a** teacher  
**I want to** add existing students to my classes  
**So that** I can manage student enrollment

**Acceptance Criteria:**
- Search/dropdown shows students at my school not in this class
- Student added immediately to class roster
- Success notification displayed
- Duplicate enrollment prevention

**Priority:** MEDIUM  
**Story Points:** 3

---

#### US-2.4: Remove Student from Class
**As a** teacher  
**I want to** remove a student from a class  
**So that** I can manage class enrollment when students move groups

**Acceptance Criteria:**
- Confirmation required before removal
- Student removed from class roster immediately
- Student account remains active (not deleted)
- Action logged for audit trail

**Priority:** MEDIUM  
**Story Points:** 2

---

### Epic 3: Analytics & Reporting

#### US-3.1: Teacher Analytics Dashboard
**As a** teacher  
**I want to** view overall statistics for all my classes  
**So that** I can track engagement and progress across my teaching

**Acceptance Criteria:**
- Display: total students, total classes, subject breakdown
- Key stage distribution chart
- Average students per class
- Recent activity timeline

**Priority:** MEDIUM  
**Story Points:** 5

---

#### US-3.2: Class-Specific Analytics
**As a** teacher  
**I want to** view detailed analytics for a specific class  
**So that** I can understand class performance and engagement

**Acceptance Criteria:**
- Student enrollment over time graph
- Subject/key stage specific metrics
- Individual student progress indicators
- Export data to CSV/PDF

**Priority:** MEDIUM  
**Story Points:** 5

---

#### US-3.3: Student Analytics View
**As a** teacher  
**I want to** view individual student analytics across all classes  
**So that** I can track student progress holistically

**Acceptance Criteria:**
- All classes student is enrolled in
- Participation/engagement metrics
- Avatar customization history
- Join date and activity log

**Priority:** LOW  
**Story Points:** 3

---

### Epic 4: School Administration

#### US-4.1: School Admin Dashboard
**As a** school admin  
**I want to** view an overview of all activity at my school  
**So that** I can monitor platform usage and engagement

**Acceptance Criteria:**
- Display: total teachers, total students, total classes
- Active users this week/month
- Subject distribution across school
- Key stage breakdown

**Priority:** HIGH  
**Story Points:** 5

---

#### US-4.2: Staff Directory
**As a** school admin  
**I want to** view all teachers registered to my school  
**So that** I can see who is using the platform

**Acceptance Criteria:**
- Table shows: teacher name, email, username, classes taught, total students
- Sortable columns
- Search/filter functionality
- Link to teacher's classes

**Priority:** HIGH  
**Story Points:** 3

---

#### US-4.3: Class Overview
**As a** school admin  
**I want to** view all classes at my school with teacher links  
**So that** I can see teaching organization school-wide

**Acceptance Criteria:**
- Table shows: class name, subject, key stage, teacher, student count
- Click teacher name to scroll/jump to their section in staff page
- Filter by subject/key stage
- Export to spreadsheet

**Priority:** MEDIUM  
**Story Points:** 3

---

#### US-4.4: School-Wide Analytics
**As a** school admin  
**I want to** view aggregated analytics for my entire school  
**So that** I can report on platform effectiveness and usage

**Acceptance Criteria:**
- Subject distribution pie chart
- Key stage enrollment bar chart
- Growth metrics (new students/classes per month)
- Most active teachers leaderboard

**Priority:** MEDIUM  
**Story Points:** 5

---

#### US-4.5: Activity Log
**As a** school admin  
**I want to** view recent activity timeline for my school  
**So that** I can monitor what's happening on the platform

**Acceptance Criteria:**
- Combined timeline of class creation and student additions
- Filterable by date range
- Includes: action type, teacher/class involved, timestamp
- Pagination for large datasets

**Priority:** LOW  
**Story Points:** 3

---

### Epic 5: Avatar System

#### US-5.1: Avatar Customization
**As a** student  
**I want to** customize my ClassDojo-style monster avatar  
**So that** I can personalize my account and feel engaged

**Acceptance Criteria:**
- Interactive canvas with monster preview
- Customization options: body color, eye shape, mouth shape, accessories
- Changes preview in real-time
- Save button persists changes to database

**Priority:** MEDIUM  
**Story Points:** 8

---

#### US-5.2: Avatar Display
**As a** user (any role)  
**I want to** see my avatar icon in the navigation bar  
**So that** I have visual confirmation of my identity

**Acceptance Criteria:**
- Avatar icon appears in top-right navbar
- Renders correctly at small size (32x32px)
- Falls back to default if no customization
- Links to avatar editor for students

**Priority:** LOW  
**Story Points:** 2

---

### Epic 6: Community Features

#### US-6.1: Teaching Resources Library
**As a** teacher  
**I want to** browse and upload teaching resources  
**So that** I can share materials with other educators

**Acceptance Criteria:**
- List view shows: title, author, subject, key stage, upload date
- Upload form accepts: files, images, PDFs, documents
- Rich text editor for resource description
- Search and filter by subject/key stage

**Priority:** MEDIUM  
**Story Points:** 8

---

#### US-6.2: Resource Comments
**As a** teacher  
**I want to** comment on teaching resources  
**So that** I can provide feedback and discuss materials

**Acceptance Criteria:**
- Comment form on resource detail page
- Comments show: author name, timestamp, content
- Edit/delete own comments only
- Nested replies (optional)

**Priority:** LOW  
**Story Points:** 5

---

#### US-6.3: Forum Discussions
**As a** teacher  
**I want to** create and participate in forum discussions  
**So that** I can collaborate with other teachers

**Acceptance Criteria:**
- Create new forum post with title and content
- Rich text editor for formatting
- Attach to subject/key stage for categorization
- View list of all posts with filters

**Priority:** MEDIUM  
**Story Points:** 8

---

#### US-6.4: Forum Replies
**As a** teacher  
**I want to** reply to forum posts  
**So that** I can engage in discussions

**Acceptance Criteria:**
- Reply form on forum detail page
- Replies show: author, timestamp, content
- Edit/delete own replies
- Quote original post (optional)

**Priority:** LOW  
**Story Points:** 3

---

### Epic 7: Accessibility

#### US-7.1: Accessibility Toolbar
**As a** user with accessibility needs  
**I want to** access an accessibility toolbar  
**So that** I can customize the interface for my needs

**Acceptance Criteria:**
- Toolbar includes: Dark Mode, High Contrast, Dyslexia Font, Text-to-Speech, Larger Text
- Settings persist across sessions (localStorage)
- Toggle switches clearly labeled
- Keyboard accessible

**Priority:** HIGH  
**Story Points:** 8

---

#### US-7.2: Screen Reader Support
**As a** visually impaired user  
**I want to** use a screen reader to navigate the platform  
**So that** I can access all features independently

**Acceptance Criteria:**
- All images have alt text
- ARIA labels on interactive elements
- Skip to main content link
- Semantic HTML structure
- Keyboard navigation support

**Priority:** HIGH  
**Story Points:** 5

---

## Sprint Planning Suggestion

### Sprint 1 (Foundation) - 2 weeks
- US-1.1: User Registration
- US-1.2: Role-Based Login
- US-2.1: Create Class
- US-7.2: Screen Reader Support

### Sprint 2 (Core Functionality) - 2 weeks
- US-1.3: Student Account Creation
- US-2.2: View Class Details
- US-2.3: Add Student to Class
- US-2.4: Remove Student from Class

### Sprint 3 (School Admin) - 2 weeks
- US-4.1: School Admin Dashboard
- US-4.2: Staff Directory
- US-4.3: Class Overview
- US-4.4: School-Wide Analytics

### Sprint 4 (Analytics) - 2 weeks
- US-3.1: Teacher Analytics Dashboard
- US-3.2: Class-Specific Analytics
- US-3.3: Student Analytics View

### Sprint 5 (Engagement) - 2 weeks
- US-5.1: Avatar Customization
- US-5.2: Avatar Display
- US-7.1: Accessibility Toolbar

### Sprint 6 (Community) - 2 weeks
- US-6.1: Teaching Resources Library
- US-6.2: Resource Comments
- US-6.3: Forum Discussions
- US-6.4: Forum Replies

### Sprint 7 (Polish) - 1 week
- US-4.5: Activity Log
- Testing and bug fixes
- Documentation updates

---

## How to Link Commits to Issues

When committing code, reference the issue number:

```bash
git commit -m "Implement role-based login redirect (closes #2)"
git commit -m "Add student removal confirmation modal (#8)"
```

GitHub will automatically link commits to issues and close them when merged.

---

## Additional Backlog Items (Future Enhancements)

- Email notifications for new students/classes
- Parent portal for viewing student progress
- Mobile app version
- Integration with school information systems
- Gamification with badges and achievements
- Calendar integration for class schedules
- Attendance tracking
- Homework assignment system
- Grade book functionality
- Real-time chat between teachers

---

**Total Story Points:** ~120 points  
**Estimated Timeline:** 7 sprints (~14 weeks)  
**Team Velocity:** Adjust based on actual sprint outcomes

---

**Next Steps:**
1. Create GitHub Issues for each user story
2. Label with epic tags (Epic-1-Auth, Epic-2-Classes, etc.)
3. Assign story points using GitHub labels
4. Move completed features to "Done" column
5. Update sprint progress weekly
