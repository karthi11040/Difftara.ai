import os
import sys
import zipfile
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding, MentorReview
from activities.models import ActivityService

PROJECTS_DATA = [
    {
        "name": "Library Management REST API",
        "description": "Intern submission for Library Management REST API with user login, book cataloging, and SQLite database storage.",
        "status": "completed",
        "category": "Education",
        "reqs": [
            ("REQ-001", "The system shall provide user login and token authentication.", "Authentication", "High", "Implemented", "app/views.py", "login_view"),
            ("REQ-002", "The system shall store book records in SQLite database models.", "Database", "High", "Implemented", "app/models.py", "Book"),
            ("REQ-003", "The system shall expose REST API endpoints for books listing.", "API", "High", "Implemented", "app/views.py", "list_books"),
            ("REQ-004", "The system shall handle safe file uploads and metadata extraction.", "File Handling", "Medium", "Partial", "app/views.py", "upload_file_handler")
        ],
        "scores": (88, 87.5, 80.0, 100.0, 100.0)
    },
    {
        "name": "E-Commerce Shopping Cart & Checkout API",
        "description": "Scalable REST API for product catalog, shopping cart state management, discount vouchers, and checkout transactions.",
        "status": "completed",
        "category": "E-Commerce",
        "reqs": [
            ("REQ-001", "The system shall authenticate customers via JWT bearer tokens.", "Authentication", "High", "Implemented", "app/views.py", "authenticate_customer"),
            ("REQ-002", "The system shall maintain persistent shopping cart items per user session.", "Database", "High", "Implemented", "app/models.py", "CartItem"),
            ("REQ-003", "The system shall expose REST endpoints to add, update, and remove cart items.", "API", "High", "Implemented", "app/views.py", "modify_cart"),
            ("REQ-004", "The system shall calculate sales tax and validate coupon discount codes.", "Business Logic", "High", "Implemented", "app/services.py", "apply_coupon"),
            ("REQ-005", "The system shall process checkout payment transactions with retry safety.", "Payments", "High", "Partial", "app/services.py", "process_payment")
        ],
        "scores": (91, 90.0, 85.0, 100.0, 100.0)
    },
    {
        "name": "Hospital Patient Portal & Appointment API",
        "description": "HIPAA-aligned patient appointment scheduling backend with doctor availability calendars and encrypted medical notes.",
        "status": "completed",
        "category": "Healthcare",
        "reqs": [
            ("REQ-001", "The system shall require multi-factor authentication for physician and patient accounts.", "Authentication", "High", "Implemented", "app/views.py", "verify_mfa_login"),
            ("REQ-002", "The system shall store appointment schedules linked to doctor profiles.", "Database", "High", "Implemented", "app/models.py", "Appointment"),
            ("REQ-003", "The system shall expose REST APIs to query open doctor time slots.", "API", "High", "Implemented", "app/views.py", "get_available_slots"),
            ("REQ-004", "The system shall encrypt patient medical records at rest.", "Security", "High", "Manual Review", "app/services.py", "encrypt_medical_record")
        ],
        "scores": (82, 81.25, 80.0, 75.0, 100.0)
    },
    {
        "name": "FinTech Wallet & Payment Gateway Service",
        "description": "Digital wallet microservice handling peer-to-peer balance transfers, ledger journaling, and automated reconciliation.",
        "status": "completed",
        "category": "FinTech",
        "reqs": [
            ("REQ-001", "The system shall authenticate API consumers with cryptographic HMAC signatures.", "Security", "High", "Implemented", "app/views.py", "verify_signature"),
            ("REQ-002", "The system shall maintain double-entry bookkeeping ledger transactions.", "Database", "High", "Implemented", "app/models.py", "LedgerEntry"),
            ("REQ-003", "The system shall support atomic balance transfer between user wallets.", "API", "High", "Implemented", "app/services.py", "transfer_funds"),
            ("REQ-004", "The system shall enforce velocity limits and fraud anomaly thresholds.", "Fraud Control", "High", "Partial", "app/services.py", "check_fraud_limits")
        ],
        "scores": (89, 87.5, 90.0, 100.0, 100.0)
    },
    {
        "name": "Student Attendance & Grade Management Portal",
        "description": "Academic records portal supporting lecture attendance logging, term exam grading, and transcript PDF generation.",
        "status": "completed",
        "category": "Education",
        "reqs": [
            ("REQ-001", "The system shall authenticate teachers and students with role-based access control.", "Authentication", "High", "Implemented", "app/views.py", "login_user"),
            ("REQ-002", "The system shall record daily student attendance timestamps per course.", "Database", "High", "Implemented", "app/models.py", "AttendanceRecord"),
            ("REQ-003", "The system shall calculate GPA weighted averages for student semesters.", "Business Logic", "Medium", "Implemented", "app/services.py", "calculate_gpa"),
            ("REQ-004", "The system shall generate student report cards as exportable documents.", "Reporting", "Medium", "Implemented", "app/views.py", "export_report_card")
        ],
        "scores": (94, 95.0, 90.0, 100.0, 100.0)
    },
    {
        "name": "Real-Time Chat & WebSocket Notification Hub",
        "description": "Real-time communication backend featuring instant messaging, presence status, typing indicators, and push notifications.",
        "status": "completed",
        "category": "Communications",
        "reqs": [
            ("REQ-001", "The system shall authenticate WebSocket connection handshakes with session tokens.", "Authentication", "High", "Implemented", "app/views.py", "ws_auth_handshake"),
            ("REQ-002", "The system shall store chat channels and message history in relational tables.", "Database", "High", "Implemented", "app/models.py", "ChatMessage"),
            ("REQ-003", "The system shall broadcast messages to channel subscribers in real time.", "Messaging", "High", "Implemented", "app/services.py", "broadcast_message"),
            ("REQ-004", "The system shall support media attachment upload and virus scanning.", "File Handling", "Medium", "Partial", "app/views.py", "upload_attachment")
        ],
        "scores": (86, 87.5, 80.0, 90.0, 100.0)
    },
    {
        "name": "Hotel Booking & Reservation Engine",
        "description": "Hospitality booking service managing room inventory, seasonal pricing tariffs, guest reservations, and automated check-ins.",
        "status": "completed",
        "category": "Travel",
        "reqs": [
            ("REQ-001", "The system shall allow guests to register and manage booking reservations.", "Authentication", "High", "Implemented", "app/views.py", "guest_signup"),
            ("REQ-002", "The system shall track room availability and pricing tiers by dates.", "Database", "High", "Implemented", "app/models.py", "RoomInventory"),
            ("REQ-003", "The system shall prevent room double-booking using transactional database locks.", "Concurrency", "High", "Implemented", "app/services.py", "reserve_room"),
            ("REQ-004", "The system shall send email confirmation receipts with reservation codes.", "Notifications", "Medium", "Implemented", "app/services.py", "send_confirmation")
        ],
        "scores": (95, 96.0, 90.0, 100.0, 100.0)
    },
    {
        "name": "Food Delivery Order & GPS Tracking Service",
        "description": "Hyper-local restaurant delivery API coordinating customer carts, driver assignment, and live geo-coordinate updates.",
        "status": "completed",
        "category": "Logistics",
        "reqs": [
            ("REQ-001", "The system shall authenticate riders, restaurants, and customers with granular roles.", "Authentication", "High", "Implemented", "app/views.py", "user_login"),
            ("REQ-002", "The system shall store restaurant menus, food items, and active orders.", "Database", "High", "Implemented", "app/models.py", "FoodOrder"),
            ("REQ-003", "The system shall assign nearby delivery drivers based on proximity calculations.", "Routing", "High", "Implemented", "app/services.py", "dispatch_driver"),
            ("REQ-004", "The system shall stream GPS coordinate telemetry updates for live order tracking.", "API", "Medium", "Implemented", "app/views.py", "update_driver_coords")
        ],
        "scores": (92, 92.5, 88.0, 95.0, 100.0)
    },
    {
        "name": "Cloud File Storage & Secure Drive API",
        "description": "Secure file storage system offering chunked multipart uploads, deduplication hashing, role sharing, and expiration links.",
        "status": "completed",
        "category": "Cloud Services",
        "reqs": [
            ("REQ-001", "The system shall provide user authentication and scoped permission checks.", "Authentication", "High", "Implemented", "app/views.py", "verify_token"),
            ("REQ-002", "The system shall store file metadata, sizes, MIME types, and SHA-256 hashes.", "Database", "High", "Implemented", "app/models.py", "StoredFile"),
            ("REQ-003", "The system shall support streaming chunked file uploads up to 5GB.", "File Handling", "High", "Partial", "app/views.py", "chunk_upload"),
            ("REQ-004", "The system shall generate temporary signed URLs for private file sharing.", "Security", "Medium", "Implemented", "app/services.py", "generate_signed_link")
        ],
        "scores": (85, 85.0, 80.0, 90.0, 100.0)
    },
    {
        "name": "IoT Smart Sensor Telemetry Aggregator",
        "description": "High-throughput telemetry ingestion service processing temperature, humidity, and vibration sensor time-series packets.",
        "status": "completed",
        "category": "IoT",
        "reqs": [
            ("REQ-001", "The system shall authenticate IoT edge devices via unique device API keys.", "Authentication", "High", "Implemented", "app/views.py", "device_auth"),
            ("REQ-002", "The system shall store time-series telemetry metrics in optimized database tables.", "Database", "High", "Implemented", "app/models.py", "TelemetryReading"),
            ("REQ-003", "The system shall evaluate sensor thresholds and trigger anomaly alerts.", "Monitoring", "High", "Implemented", "app/services.py", "evaluate_thresholds"),
            ("REQ-004", "The system shall aggregate hourly rolling averages for dashboard graphs.", "Analytics", "Medium", "Implemented", "app/views.py", "get_device_metrics")
        ],
        "scores": (93, 94.0, 90.0, 90.0, 100.0)
    },
    {
        "name": "Social Network Feed & Media Sharing API",
        "description": "Social graph backend with following relationships, fanout-on-write newsfeed timelines, likes, comments, and media tags.",
        "status": "completed",
        "category": "Social Media",
        "reqs": [
            ("REQ-001", "The system shall support user signup, profile updates, and JWT sessions.", "Authentication", "High", "Implemented", "app/views.py", "profile_auth"),
            ("REQ-002", "The system shall model user followers, posts, comments, and likes.", "Database", "High", "Implemented", "app/models.py", "Post"),
            ("REQ-003", "The system shall generate personalized chronologically ordered feeds.", "Algorithms", "High", "Implemented", "app/services.py", "build_user_feed"),
            ("REQ-004", "The system shall sanitize and filter profanity in user comments.", "Content Moderation", "Medium", "Partial", "app/services.py", "filter_profanity")
        ],
        "scores": (87, 87.5, 82.0, 95.0, 100.0)
    },
    {
        "name": "Online Proctoring & Examination System",
        "description": "Secure online examination platform featuring randomized question banks, timed quiz sessions, and proctor event logs.",
        "status": "completed",
        "category": "Education",
        "reqs": [
            ("REQ-001", "The system shall authenticate examinees and verify session tokens.", "Authentication", "High", "Implemented", "app/views.py", "student_exam_login"),
            ("REQ-002", "The system shall store question pools, options, correct answers, and submissions.", "Database", "High", "Implemented", "app/models.py", "ExamSubmission"),
            ("REQ-003", "The system shall automatically grade objective multiple-choice submissions.", "Grading", "High", "Implemented", "app/services.py", "auto_grade_exam"),
            ("REQ-004", "The system shall record tab-switch and focus-loss proctoring violations.", "Security", "Medium", "Implemented", "app/views.py", "log_proctor_event")
        ],
        "scores": (96, 97.0, 92.0, 100.0, 100.0)
    },
    {
        "name": "Smart Fleet Logistics & Route Dispatch Engine",
        "description": "Fleet telematics and route optimization service tracking vehicle maintenance, cargo manifest logs, and fuel economy.",
        "status": "completed",
        "category": "Transportation",
        "reqs": [
            ("REQ-001", "The system shall provide dispatcher login and vehicle driver credentials.", "Authentication", "High", "Implemented", "app/views.py", "fleet_login"),
            ("REQ-002", "The system shall track vehicle inventory, odometer readings, and cargo manifests.", "Database", "High", "Implemented", "app/models.py", "VehicleManifest"),
            ("REQ-003", "The system shall compute optimal delivery route waypoints.", "Optimization", "High", "Partial", "app/services.py", "optimize_route"),
            ("REQ-004", "The system shall alert operators when maintenance inspection intervals expire.", "Maintenance", "Medium", "Implemented", "app/services.py", "check_maintenance_due")
        ],
        "scores": (84, 85.0, 80.0, 85.0, 100.0)
    },
    {
        "name": "Employee Payroll & HR Management Service",
        "description": "Enterprise HR service managing employee records, paid time off (PTO) requests, tax deduction schedules, and salary disbursements.",
        "status": "completed",
        "category": "Enterprise",
        "reqs": [
            ("REQ-001", "The system shall enforce role-based access for HR staff and general employees.", "Authentication", "High", "Implemented", "app/views.py", "hr_login"),
            ("REQ-002", "The system shall store employee compensation structures and bank payout details.", "Database", "High", "Implemented", "app/models.py", "PayrollRecord"),
            ("REQ-003", "The system shall calculate net salary with statutory tax and pension deductions.", "Payroll Logic", "High", "Implemented", "app/services.py", "calculate_payroll"),
            ("REQ-004", "The system shall manage PTO leave balances and supervisor approval workflows.", "Workflow", "Medium", "Implemented", "app/views.py", "submit_leave_request")
        ],
        "scores": (93, 93.5, 90.0, 95.0, 100.0)
    },
    {
        "name": "Crypto Portfolio & Real-Time Market Tracker",
        "description": "Investment tracking dashboard calculating portfolio profit/loss, historical price charts, and automated price alert webhooks.",
        "status": "completed",
        "category": "FinTech",
        "reqs": [
            ("REQ-001", "The system shall authenticate investors with encrypted session keys.", "Authentication", "High", "Implemented", "app/views.py", "investor_login"),
            ("REQ-002", "The system shall record buy/sell crypto transactions and cost basis records.", "Database", "High", "Implemented", "app/models.py", "CryptoTransaction"),
            ("REQ-003", "The system shall calculate real-time portfolio net asset value and returns.", "Analytics", "High", "Implemented", "app/services.py", "calculate_portfolio_value"),
            ("REQ-004", "The system shall dispatch webhook alerts when cryptocurrency price limits cross.", "Notifications", "Medium", "Partial", "app/services.py", "trigger_price_alert")
        ],
        "scores": (88, 88.0, 85.0, 90.0, 100.0)
    },
    {
        "name": "Learning Management System (LMS) Portal",
        "description": "Online e-learning course management platform with video syllabus milestones, homework assignments, and certificates.",
        "status": "completed",
        "category": "Education",
        "reqs": [
            ("REQ-001", "The system shall authenticate students and instructors with distinct roles.", "Authentication", "High", "Implemented", "app/views.py", "lms_login"),
            ("REQ-002", "The system shall store courses, modules, video lessons, and student enrollments.", "Database", "High", "Implemented", "app/models.py", "CourseEnrollment"),
            ("REQ-003", "The system shall track student lesson completion percentage and progress.", "Progress", "High", "Implemented", "app/services.py", "track_course_progress"),
            ("REQ-004", "The system shall issue completion certificates upon 100% course fulfillment.", "Certificates", "Medium", "Implemented", "app/services.py", "generate_certificate")
        ],
        "scores": (95, 95.5, 92.0, 100.0, 100.0)
    },
    {
        "name": "Customer Relationship Management (CRM) Pipeline",
        "description": "Sales CRM backend with deal stage pipelines, contact address book, interaction audit notes, and revenue projections.",
        "status": "completed",
        "category": "Enterprise",
        "reqs": [
            ("REQ-001", "The system shall authenticate sales representatives and team managers.", "Authentication", "High", "Implemented", "app/views.py", "crm_login"),
            ("REQ-002", "The system shall store lead contacts, deal stages, and deal financial values.", "Database", "High", "Implemented", "app/models.py", "SalesLead"),
            ("REQ-003", "The system shall support dragging deals through Kanban pipeline stages.", "API", "High", "Implemented", "app/views.py", "update_deal_stage"),
            ("REQ-004", "The system shall forecast quarterly sales revenue based on deal probability.", "Forecasting", "Medium", "Implemented", "app/services.py", "forecast_pipeline_revenue")
        ],
        "scores": (91, 91.0, 88.0, 95.0, 100.0)
    },
    {
        "name": "AI Resume Parser & Candidate Matcher",
        "description": "Recruitment automation microservice extracting skills from PDF resumes and ranking candidate match scores for job postings.",
        "status": "completed",
        "category": "AI / ML",
        "reqs": [
            ("REQ-001", "The system shall provide recruiter authentication and hiring permissions.", "Authentication", "High", "Implemented", "app/views.py", "recruiter_login"),
            ("REQ-002", "The system shall store job vacancies, applicant profiles, and parsed resume entities.", "Database", "High", "Implemented", "app/models.py", "JobApplication"),
            ("REQ-003", "The system shall extract key programming skills and certifications from uploaded resumes.", "NLP", "High", "Implemented", "app/services.py", "parse_resume_skills"),
            ("REQ-004", "The system shall score candidate fit against job requirement keywords.", "Matching", "High", "Implemented", "app/services.py", "match_candidate_score")
        ],
        "scores": (90, 90.0, 86.0, 95.0, 100.0)
    },
    {
        "name": "Event Ticketing & Seat Reservation Platform",
        "description": "Live concert ticketing API handling venue seat maps, reservation locks, barcode ticket generation, and turnstile check-in.",
        "status": "completed",
        "category": "Entertainment",
        "reqs": [
            ("REQ-001", "The system shall authenticate concert attendees and venue gate staff.", "Authentication", "High", "Implemented", "app/views.py", "ticket_auth"),
            ("REQ-002", "The system shall store venue seating sections, ticket tiers, and event schedules.", "Database", "High", "Implemented", "app/models.py", "EventTicket"),
            ("REQ-003", "The system shall temporarily hold seats for 10 minutes during checkout.", "Concurrency", "High", "Implemented", "app/services.py", "hold_seats_transaction"),
            ("REQ-004", "The system shall generate unique scannable QR ticket barcodes upon purchase.", "Ticketing", "Medium", "Implemented", "app/services.py", "generate_ticket_qr")
        ],
        "scores": (94, 94.5, 90.0, 100.0, 100.0)
    },
    {
        "name": "Smart Home IoT Automation Hub",
        "description": "Home automation controller managing lighting scenes, smart thermostat schedules, security cameras, and voice intent hooks.",
        "status": "completed",
        "category": "Smart Home",
        "reqs": [
            ("REQ-001", "The system shall authenticate mobile app controls with secure device tokens.", "Authentication", "High", "Implemented", "app/views.py", "hub_auth"),
            ("REQ-002", "The system shall store device hardware models, state values, and automation rules.", "Database", "High", "Implemented", "app/models.py", "SmartDevice"),
            ("REQ-003", "The system shall execute scene routines based on cron schedules or trigger sensors.", "Automation", "High", "Implemented", "app/services.py", "trigger_scene_automation"),
            ("REQ-004", "The system shall log energy wattage consumption statistics across rooms.", "Energy", "Medium", "Partial", "app/views.py", "get_energy_report")
        ],
        "scores": (87, 87.5, 82.0, 90.0, 100.0)
    },
    {
        "name": "Pharmacy Inventory & Prescription Verification",
        "description": "Healthcare supply chain API managing medicine stock batches, expiration alerts, doctor prescription verification, and refills.",
        "status": "completed",
        "category": "Healthcare",
        "reqs": [
            ("REQ-001", "The system shall authenticate licensed pharmacists and doctor prescribers.", "Authentication", "High", "Implemented", "app/views.py", "pharma_login"),
            ("REQ-002", "The system shall store medicine batch numbers, expiry dates, and shelf quantities.", "Database", "High", "Implemented", "app/models.py", "MedicineBatch"),
            ("REQ-003", "The system shall validate prescription doctor credentials before dispensing drugs.", "Compliance", "High", "Implemented", "app/services.py", "validate_prescription"),
            ("REQ-004", "The system shall flag medicines nearing expiration within 60 days.", "Inventory", "Medium", "Implemented", "app/services.py", "get_expiring_batches")
        ],
        "scores": (92, 92.5, 88.0, 95.0, 100.0)
    },
    {
        "name": "Recipe Sharing & Meal Planner API",
        "description": "Culinary community API for discovering recipes, generating weekly meal plans, calculating nutritional macros, and grocery lists.",
        "status": "completed",
        "category": "Food & Beverage",
        "reqs": [
            ("REQ-001", "The system shall support user authentication and author profiles.", "Authentication", "High", "Implemented", "app/views.py", "user_auth"),
            ("REQ-002", "The system shall store recipes, ingredients, instructions, and community ratings.", "Database", "High", "Implemented", "app/models.py", "Recipe"),
            ("REQ-003", "The system shall aggregate grocery shopping lists from planned weekly menus.", "Meal Planning", "Medium", "Implemented", "app/services.py", "build_grocery_list"),
            ("REQ-004", "The system shall calculate total calories and macronutrients per serving.", "Nutrition", "Medium", "Implemented", "app/services.py", "calculate_macros")
        ],
        "scores": (93, 93.0, 89.0, 100.0, 100.0)
    },
    {
        "name": "Video On Demand Streaming & Transcoding API",
        "description": "Video delivery platform managing media catalog, adaptive HLS bitrate playback playlists, and user viewing timestamps.",
        "status": "completed",
        "category": "Media",
        "reqs": [
            ("REQ-001", "The system shall authenticate subscribers and verify active membership plans.", "Authentication", "High", "Implemented", "app/views.py", "subscriber_login"),
            ("REQ-002", "The system shall store video metadata, multi-resolution manifests, and watch history.", "Database", "High", "Implemented", "app/models.py", "VideoContent"),
            ("REQ-003", "The system shall resume video playback from last saved timestamp position.", "Playback", "High", "Implemented", "app/views.py", "save_playback_position"),
            ("REQ-004", "The system shall generate adaptive HLS streaming playlist manifests.", "Streaming", "High", "Manual Review", "app/services.py", "build_hls_manifest")
        ],
        "scores": (81, 81.25, 78.0, 85.0, 100.0)
    },
    {
        "name": "Fitness Tracking & Workout Analytics Engine",
        "description": "Wearable activity tracker API synchronizing step counts, heart rate zones, calories burned, and personal workout goals.",
        "status": "completed",
        "category": "Health & Fitness",
        "reqs": [
            ("REQ-001", "The system shall authenticate athletes and secure health biometric metrics.", "Authentication", "High", "Implemented", "app/views.py", "athlete_auth"),
            ("REQ-002", "The system shall store workout exercises, heart rate logs, and calorie calculations.", "Database", "High", "Implemented", "app/models.py", "WorkoutSession"),
            ("REQ-003", "The system shall summarize weekly progress towards target calorie burning goals.", "Analytics", "Medium", "Implemented", "app/services.py", "calculate_weekly_summary"),
            ("REQ-004", "The system shall trigger achievement milestone badges upon completing milestones.", "Gamification", "Low", "Implemented", "app/services.py", "award_badges")
        ],
        "scores": (96, 96.5, 92.0, 100.0, 100.0)
    },
    {
        "name": "Bug Tracker & Agile Sprint Kanban API",
        "description": "Engineering issue tracking service featuring sprint backlogs, bug severity levels, git commit cross-linking, and burndown charts.",
        "status": "completed",
        "category": "Developer Tools",
        "reqs": [
            ("REQ-001", "The system shall authenticate developers and manage organization permissions.", "Authentication", "High", "Implemented", "app/views.py", "developer_login"),
            ("REQ-002", "The system shall store ticket issues, sprint milestones, labels, and assignment.", "Database", "High", "Implemented", "app/models.py", "BugIssue"),
            ("REQ-003", "The system shall support transitioning tickets between Kanban workflow stages.", "Workflow", "High", "Implemented", "app/views.py", "transition_issue"),
            ("REQ-004", "The system shall calculate sprint velocity and burndown chart metrics.", "Agile Reporting", "Medium", "Implemented", "app/services.py", "calculate_sprint_burndown")
        ],
        "scores": (95, 95.0, 90.0, 100.0, 100.0)
    }
]

STUDENT_USERNAMES = [
    ("student", "Student Demo"),
    ("arun_kumar", "Arun Kumar"),
    ("priya_sharma", "Priya Sharma"),
    ("vikram_singh", "Vikram Singh"),
    ("neha_patel", "Neha Patel"),
    ("rahul_verma", "Rahul Verma"),
    ("ananya_iyer", "Ananya Iyer"),
    ("kavita_reddy", "Kavita Reddy"),
    ("aditya_joshi", "Aditya Joshi"),
    ("meera_nair", "Meera Nair")
]

def make_source_code(project_info):
    name = project_info["name"]
    reqs = project_info["reqs"]
    
    # Generate python views.py
    views_lines = [
        "import json",
        "from django.http import JsonResponse",
        "from django.views.decorators.csrf import csrf_exempt",
        "",
        f"# Views implementation for {name}",
        ""
    ]
    for req in reqs:
        fn_name = req[6] if len(req) > 6 and req[6] != "N/A" and "(" not in req[6] else "handler_" + req[0].replace("-", "_").lower()
        views_lines.extend([
            f"def {fn_name}(request):",
            f'    """Fulfills {req[0]}: {req[1]}"""',
            "    try:",
            "        if request.method == 'POST':",
            "            data = json.loads(request.body) if request.body else {}",
            f"            return JsonResponse({{'status': 'success', 'module': '{req[2]}', 'data': data}})",
            f"        return JsonResponse({{'status': 'active', 'description': '{req[1]}'}})",
            "    except Exception as e:",
            "        return JsonResponse({'error': str(e)}, status=400)",
            ""
        ])

    views_code = "\n".join(views_lines)

    # Generate models.py
    models_lines = [
        "from django.db import models",
        "",
        f"# Data models for {name}",
        ""
    ]
    for req in reqs:
        model_name = req[6] if len(req) > 6 and req[6][0].isupper() else f"{req[2].replace(' ', '')}Model"
        models_lines.extend([
            f"class {model_name}(models.Model):",
            "    title = models.CharField(max_length=200)",
            "    status = models.CharField(max_length=50, default='active')",
            "    created_at = models.DateTimeField(auto_now_add=True)",
            "    updated_at = models.DateTimeField(auto_now=True)",
            "",
            "    def __str__(self):",
            "        return self.title",
            ""
        ])
    models_code = "\n".join(models_lines)

    # Generate services.py
    services_lines = [
        "# Business logic services",
        "import math",
        "import datetime",
        "",
        f"class {name.replace(' ', '').replace('&', '').replace('-', '')}Service:",
        "    @staticmethod",
        "    def execute_workflow(payload):",
        "        try:",
        "            timestamp = datetime.datetime.now()",
        "            return {'success': True, 'timestamp': str(timestamp)}",
        "        except Exception as e:",
        "            return {'success': False, 'error': str(e)}",
        ""
    ]
    for req in reqs:
        if "services.py" in (req[5] if len(req) > 5 else ""):
            fn_name = req[6] if len(req) > 6 else "process"
            services_lines.extend([
                f"    @staticmethod",
                f"    def {fn_name}(data):",
                f'        """Service helper for {req[1]}"""',
                "        try:",
                "            return {'processed': True, 'input': data}",
                "        except Exception as e:",
                "            return {'error': str(e)}",
                ""
            ])
    services_code = "\n".join(services_lines)

    # Generate tests.py
    tests_code = f"""import unittest

class Test{name.replace(' ', '').replace('&', '').replace('-', '')}(unittest.TestCase):
    def test_initialization(self):
        self.assertTrue(True)

    def test_requirements_compliance(self):
        self.assertEqual(1 + 1, 2)

    def test_status_response(self):
        self.assertIsNotNone("active")
"""

    readme_code = f"""# {name}

## Project Overview
{project_info["description"]}

## Category
{project_info["category"]}

## Implemented Requirements
""" + "\n".join([f"- **{r[0]}**: {r[1]} ({r[2]})" for r in reqs]) + """

## Installation & Running
```bash
python manage.py migrate
python manage.py runserver
```
"""

    return {
        "README.md": readme_code,
        "app/views.py": views_code,
        "app/models.py": models_code,
        "app/services.py": services_code,
        "tests/test_api.py": tests_code
    }


def seed_25():
    print("Beginning seeding of 25 comprehensive projects...")
    
    # 1. Ensure Users
    sanjay_user, _ = User.objects.get_or_create(username='SanjayS', defaults={'email': 'sanjays@example.com', 'role': User.ADMIN})
    sanjay_user.set_password('Sanjay_8821')
    sanjay_user.is_superuser = True
    sanjay_user.is_staff = True
    sanjay_user.save()

    mentor_user, _ = User.objects.get_or_create(username='mentor', defaults={'email': 'mentor@example.com', 'role': User.MENTOR})
    mentor_user.set_password('Sanjay_8821')
    mentor_user.is_staff = True
    mentor_user.save()

    students = []
    for uname, fname in STUDENT_USERNAMES:
        u, _ = User.objects.get_or_create(username=uname, defaults={'email': f'{uname}@example.com', 'role': User.STUDENT})
        u.set_password('Sanjay_8821')
        u.save()
        students.append(u)

    print(f"Users confirmed: SanjayS, mentor, and {len(students)} student demo accounts.")

    # 2. Iterate and create 25 projects
    zip_dir = os.path.join(settings.MEDIA_ROOT, 'zips')
    extracted_base = os.path.join(settings.MEDIA_ROOT, 'extracted')
    os.makedirs(zip_dir, exist_ok=True)
    os.makedirs(extracted_base, exist_ok=True)

    created_count = 0

    for idx, pdata in enumerate(PROJECTS_DATA, start=1):
        pname = pdata["name"]
        assigned_student = students[(idx - 1) % len(students)]
        
        # Prepare zip file
        zip_filename = f"project_{idx}_{pname.lower().replace(' ', '_').replace('&', 'and')[:30]}.zip"
        zip_full_path = os.path.join(zip_dir, zip_filename)
        rel_zip_path = f"zips/{zip_filename}"

        # Source code files
        files_dict = make_source_code(pdata)
        with zipfile.ZipFile(zip_full_path, 'w') as zf:
            for filepath, content in files_dict.items():
                zf.writestr(filepath, content.strip())

        # Extract target directory
        project, created = Project.objects.get_or_create(
            name=pname,
            defaults={
                "description": pdata["description"],
                "owner": assigned_student,
                "zip_file": rel_zip_path,
                "status": pdata["status"]
            }
        )

        extract_target_dir = os.path.join(extracted_base, str(project.id))
        os.makedirs(extract_target_dir, exist_ok=True)
        for filepath, content in files_dict.items():
            full_out = os.path.join(extract_target_dir, filepath.replace('/', os.sep))
            os.makedirs(os.path.dirname(full_out), exist_ok=True)
            with open(full_out, 'w', encoding='utf-8') as f:
                f.write(content.strip())

        project.extracted_path = extract_target_dir
        project.save()

        # Create Requirements
        req_objs = []
        for r_id, r_desc, r_cat, r_prio, st, ev_file, ev_fn in pdata["reqs"]:
            req_obj, _ = Requirement.objects.get_or_create(
                project=project,
                requirement_id=r_id,
                defaults={
                    "description": r_desc,
                    "category": r_cat,
                    "priority": r_prio,
                    "active": True
                }
            )
            req_objs.append((req_obj, st, ev_file, ev_fn))

        # Create or update Review
        review = project.reviews.first()
        scores = pdata["scores"]
        if not review:
            review = Review.objects.create(
                project=project,
                mentor=mentor_user,
                status='completed',
                overall_score=scores[0],
                compliance_score=scores[1],
                quality_score=scores[2],
                testing_score=scores[3],
                doc_score=scores[4]
            )
        else:
            review.overall_score = scores[0]
            review.compliance_score = scores[1]
            review.quality_score = scores[2]
            review.testing_score = scores[3]
            review.doc_score = scores[4]
            review.save()

        # Create Findings if not already populated
        if review.findings.count() == 0:
            for req_obj, st, ev_file, ev_fn in req_objs:
                finding = Finding.objects.create(
                    review=review,
                    requirement=req_obj,
                    status=st,
                    evidence_file=ev_file,
                    evidence_function=ev_fn,
                    description=f"Requirement [{req_obj.requirement_id}] matched implementation pattern in source code.",
                    suggestion=f"Ensure comprehensive error checking and integration tests for {ev_fn}." if st == 'Implemented' else f"Complete missing edge case validation for {req_obj.requirement_id}.",
                    priority=req_obj.priority
                )

                # Add a sample mentor override on select partial findings
                if st == 'Partial' and idx % 3 == 0:
                    MentorReview.objects.create(
                        finding=finding,
                        reviewer=mentor_user,
                        original_status='Partial',
                        final_status='Implemented',
                        comment="Verified edge cases in service layer during code walkthrough. Upgraded status to Implemented."
                    )

            # Add general quality finding
            Finding.objects.create(
                review=review,
                requirement=None,
                status='Implemented' if scores[2] >= 85 else 'Partial',
                evidence_file='app/views.py',
                evidence_function='N/A',
                description="[Quality] PEP8 Compliance & AST Structure: Project conforms to standard Python architecture conventions.",
                suggestion="Maintain modular helper functions and maintain high test coverage.",
                priority='Medium'
            )

        # Record activity logs
        ActivityService.record(
            user=assigned_student,
            project=project,
            action='UPLOAD_PROJECT',
            message=f"Uploaded project ZIP '{project.name}' successfully."
        )
        ActivityService.record(
            user=mentor_user,
            project=project,
            action='REVIEW_RUN',
            message=f"Completed automated review for project '{project.name}' with score {scores[0]}%."
        )

        created_count += 1
        print(f"[{created_count}/25] Configured project: '{pname}' (Score: {scores[0]}%)")

    print(f"\nSuccessfully seeded all {created_count} projects with complete requirements, reviews, findings, and reports!")

if __name__ == '__main__':
    seed_25()
