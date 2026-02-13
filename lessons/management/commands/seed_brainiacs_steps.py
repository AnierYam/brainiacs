from django.core.management.base import BaseCommand

from lessons.models import Badge, Step


class Command(BaseCommand):
    help = "Seed Brainiacs steps and badges for Missions 2-4."

    def handle(self, *args, **options):
        badges = [
            # Mission 2
            {
                "slug": "arduino-rookie",
                "name": "Arduino Rookie",
                "description": "You met the Arduino board and its parts.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-2-arduino-board",
            },
            {
                "slug": "circuit-starter",
                "name": "Circuit Starter",
                "description": "You explored the breadboard connections.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-2-breadboard",
            },
            {
                "slug": "code-explorer",
                "name": "Code Explorer",
                "description": "You toured the Arduino IDE and tools.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-2-arduino-ide",
            },
            {
                "slug": "brain-powered",
                "name": "Brain Powered",
                "description": "You completed Mission 2.",
                "xp_reward": 0,
                "rule_type": "mission_complete",
                "rule_target": "mission-2",
            },
            # Mission 3
            {
                "slug": "body-builder",
                "name": "Body Builder",
                "description": "You built Pedro's body system.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-3-system-1",
            },
            {
                "slug": "eye-engineer",
                "name": "Eye Engineer",
                "description": "You finished Pedro's head system.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-3-system-2",
            },
            {
                "slug": "tail-tamer",
                "name": "Tail Tamer",
                "description": "You completed Pedro's tail system.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-3-system-3",
            },
            {
                "slug": "legs-engineer",
                "name": "Legs Engineer",
                "description": "You built Pedro's leg systems.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-3-system-4-right",
            },
            {
                "slug": "stand-specialist",
                "name": "Stand Specialist",
                "description": "You finished Pedro's stand system.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-3-system-5",
            },
            {
                "slug": "system-master",
                "name": "System Master",
                "description": "You completed Mission 3.",
                "xp_reward": 0,
                "rule_type": "mission_complete",
                "rule_target": "mission-3",
            },
            # Mission 4
            {
                "slug": "power-master",
                "name": "Power Master",
                "description": "You wired up Pedro's power.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-4",
            },
            {
                "slug": "code-combiner",
                "name": "Code Combiner",
                "description": "You merged all the code into one program.",
                "xp_reward": 0,
                "rule_type": "group_complete",
                "rule_target": "mission-4",
            },
            {
                "slug": "pedro-alive",
                "name": "Pedro Alive",
                "description": "You completed Mission 4.",
                "xp_reward": 0,
                "rule_type": "mission_complete",
                "rule_target": "mission-4",
            },
        ]

        steps = []

        def add_step(
            slug,
            title,
            parent_slug,
            order,
            content_mode,
            has_quiz,
            xp_on_complete,
            xp_on_quiz_correct,
        ):
            steps.append(
                {
                    "slug": slug,
                    "title": title,
                    "parent_slug": parent_slug,
                    "order": order,
                    "content_mode": content_mode,
                    "has_quiz": has_quiz,
                    "xp_on_complete": xp_on_complete,
                    "xp_on_quiz_correct": xp_on_quiz_correct,
                }
            )

        quiz_xp = 15

        # Mission 2 - Arduino Board (cards, unit ordering)
        order = 1
        parent = "mission-2-arduino-board"
        add_step("introduction", "Meet the Arduino", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("power-input", "Power Connector", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("usb-input", "USB Power Port", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("on-led", "Power On Light", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("microcontroller", "The Brain Chip", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("reset-button", "Reset Button", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("tx-rx-lights", "TX/RX Lights", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("l-led", "The L Light (Pin 13 LED)", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("checkpoint-quiz", "Checkpoint Quiz", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("digital-vs-analog", "Digital vs Analog", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("power-output", "Analog Input / Output", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("arduino-pinout", "Digital Input / Output", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("arduino-board-quiz", "Checkpoint Quiz", parent, order, "cards", True, 10, quiz_xp)

        # Mission 2 - Breadboard (cards, emoji titles)
        order = 1
        parent = "mission-2-breadboard"
        add_step("what-is-a-breadboard", "\U0001F4CB Breadboard Basics", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("breadboard-power-rails", "\u26A1 Power Rails", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("row-and-column-connections", "\U0001F9E9 Rows & Columns", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("connect-your-breadboard", "\U0001F517 Connect the Board", parent, order, "cards", False, 10, 0)
        order += 1
        add_step("build-your-first-circuit", "\U0001F4A1 First Circuit", parent, order, "cards", False, 10, 0)

        # Mission 2 - Arduino IDE (cards, emoji titles)
        order = 1
        parent = "mission-2-arduino-ide"
        add_step("installing-the-arduino-ide", "\u2B07 Install the IDE", parent, order, "cards", False, 10, 0)
        order += 1
        add_step("understand-the-arduino-ide", "\U0001F9ED IDE Tour", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("the-serial-monitor", "\U0001F6F0 Serial Monitor", parent, order, "cards", True, 10, quiz_xp)
        order += 1
        add_step("upload-your-first-code", "\U0001F680 Upload Your First Code", parent, order, "cards", False, 10, 0)

        # Mission 3 - System 1 (all video)
        order = 1
        parent = "mission-3-system-1"
        add_step("body-leg-connector-front", "Front Connectors", parent, order, "video", False, 15, 0)
        order += 1
        add_step("body-leg-connector-back", "Back Connectors", parent, order, "video", False, 15, 0)
        order += 1
        add_step("build-structure", "The Body Structure", parent, order, "video", False, 15, 0)

        # Mission 3 - System 2 (video + cards)
        order = 1
        parent = "mission-3-system-2"
        add_step("build-head", "The Head", parent, order, "video", False, 15, 0)
        order += 1
        add_step("head-electronics", "Connecting the Eyes", parent, order, "cards", True, 15, quiz_xp)
        order += 1
        add_step("head-code", "Coding the Eyes", parent, order, "cards", True, 20, quiz_xp)

        # Mission 3 - System 3 (video + cards)
        order = 1
        parent = "mission-3-system-3"
        add_step("tail-structure", "The Tail", parent, order, "video", False, 15, 0)
        order += 1
        add_step("tail-electronics", "Connecting the Tail", parent, order, "cards", True, 15, quiz_xp)
        order += 1
        add_step("tail-code", "Coding the Tail", parent, order, "cards", True, 20, quiz_xp)

        # Mission 3 - System 4 Left (video)
        order = 1
        parent = "mission-3-system-4-left"
        add_step("legs-left-structure", "The Left Legs", parent, order, "video", False, 15, 0)

        # Mission 3 - System 4 Right (video + cards)
        order = 1
        parent = "mission-3-system-4-right"
        add_step("legs-right-structure", "The Right Legs", parent, order, "video", False, 15, 0)
        order += 1
        add_step("legs-right-electronics", "Connecting the Motor", parent, order, "cards", True, 15, quiz_xp)
        order += 1
        add_step("legs-right-code", "Coding the Motor", parent, order, "cards", True, 20, quiz_xp)

        # Mission 3 - System 5 (video)
        order = 1
        parent = "mission-3-system-5"
        add_step("stand-structure", "The Stand", parent, order, "video", False, 15, 0)

        # Mission 4 - Assembly
        order = 1
        parent = "mission-4"
        add_step("assemble-frame", "The Assembly", parent, order, "video", False, 15, 0)
        order += 1
        add_step("final-wiring", "Wiring Power", parent, order, "cards", True, 15, quiz_xp)
        order += 1
        add_step("combine-code", "Combine the Code", parent, order, "cards", True, 20, quiz_xp)
        order += 1
        add_step("power-switch", "Power Switch", parent, order, "cards", True, 15, quiz_xp)

        created_badges = 0
        updated_badges = 0
        for data in badges:
            _, created = Badge.objects.update_or_create(slug=data["slug"], defaults=data)
            if created:
                created_badges += 1
            else:
                updated_badges += 1

        created_steps = 0
        updated_steps = 0
        for data in steps:
            _, created = Step.objects.update_or_create(
                slug=data["slug"],
                parent_slug=data["parent_slug"],
                defaults=data,
            )
            if created:
                created_steps += 1
            else:
                updated_steps += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Badges seeded. Created: {created_badges}, Updated: {updated_badges}."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Steps seeded. Created: {created_steps}, Updated: {updated_steps}."
            )
        )
        self.stdout.write("Run: python manage.py seed_brainiacs_steps")
