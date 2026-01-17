from django.core.management.base import BaseCommand

from levels.models import Badge, Step


class Command(BaseCommand):
    help = "Seed gamification steps and badges for Missions 1-4."

    def handle(self, *args, **options):
        steps = []

        def add_step(
            mission_number,
            slug,
            title,
            order,
            content_mode="info",
            is_quiz=False,
            xp_reward=None,
            group_slug="",
        ):
            steps.append(
                {
                    "mission_number": mission_number,
                    "group_slug": group_slug,
                    "slug": slug,
                    "title": title,
                    "order": order,
                    "content_mode": content_mode,
                    "is_quiz": is_quiz,
                    "xp_reward": xp_reward,
                }
            )

        # Mission 1: Tools / Fasteners / Pedro Parts
        order = 1
        add_step(1, "cross-head-screwdriver", "Cross-head Screwdriver", order)
        order += 1
        add_step(1, "combination-wrench", "Combination Wrench", order)
        order += 1
        add_step(1, "part-1-quiz", "Tools Quiz", order, is_quiz=True, xp_reward=15)
        order += 1
        add_step(1, "screws", "Bolts", order)
        order += 1
        add_step(1, "plain-washers", "Plain Washers", order)
        order += 1
        add_step(1, "spring-washers", "Spring Washers", order)
        order += 1
        add_step(1, "nuts", "Nuts", order)
        order += 1
        add_step(1, "torque-nuts", "Torque Nuts", order)
        order += 1
        add_step(1, "part-2-quiz", "Fasteners Quiz", order, is_quiz=True, xp_reward=15)
        order += 1
        add_step(1, "assembly-parts", "Discover Pedro Parts", order)

        # Mission 2: Arduino Board, Breadboard, Arduino IDE
        order = 1
        lesson1 = [
            ("introduction", "Introduction", "cards"),
            ("usb-input", "USB Input", "info"),
            ("power-input", "Power Input", "info"),
            ("reset-button", "Reset Button", "info"),
            ("microcontroller", "The Microcontroller", "info"),
            ("power-output", "Power Output", "info"),
            ("digital-vs-analog", "Digital vs. Analog", "info"),
            ("arduino-pinout", "The Arduino Pinout", "info"),
        ]
        for slug, title, mode in lesson1:
            add_step(2, slug, title, order, content_mode=mode)
            order += 1

        lesson2 = [
            ("what-is-a-breadboard", "Introduction", "info"),
            ("breadboard-power-rails", "Power Rails", "info"),
            ("row-and-column-connections", "Row and Column Connections", "info"),
            ("connect-your-breadboard", "Connect Your Board", "info"),
            ("build-your-first-circuit", "Build Your First Circuit", "info"),
        ]
        for slug, title, mode in lesson2:
            add_step(2, slug, title, order, content_mode=mode)
            order += 1

        lesson3 = [
            ("installing-the-arduino-ide", "Installation", "info"),
            ("understand-the-arduino-ide", "Understanding the IDE", "info"),
            ("the-serial-monitor", "The Serial Monitor", "info"),
            ("upload-your-first-code", "Upload Your First Code", "info"),
        ]
        for slug, title, mode in lesson3:
            add_step(2, slug, title, order, content_mode=mode)
            order += 1

        # Mission 3: 5 systems
        order = 1
        video_steps = {
            "body-leg-connector-front",
            "body-leg-connector-back",
            "build-structure",
            "build-head",
            "tail-structure",
            "legs-left-structure",
            "legs-right-structure",
            "stand-structure",
        }
        mission3_systems = [
            (
                "pedro-body",
                [
                    ("body-leg-connector-front", "Front Connectors"),
                    ("body-leg-connector-back", "Back Connectors"),
                    ("build-structure", "The Body Structure"),
                ],
            ),
            (
                "pedro-head",
                [
                    ("build-head", "The Head"),
                    ("head-electronics", "Connecting the Eyes"),
                    ("head-code", "Coding the Eyes"),
                ],
            ),
            (
                "pedro-tail",
                [
                    ("tail-structure", "The Tail"),
                    ("tail-electronics", "Connecting the Tail"),
                    ("tail-code", "Coding the Tail"),
                ],
            ),
            (
                "pedro-legs-left",
                [
                    ("legs-left-structure", "The Left Legs"),
                ],
            ),
            (
                "pedro-legs-right",
                [
                    ("legs-right-structure", "The Right Legs"),
                    ("legs-right-electronics", "Connecting the Motor"),
                    ("legs-right-code", "Coding the Motor"),
                ],
            ),
            (
                "pedro-battery",
                [
                    ("stand-structure", "The Stand"),
                ],
            ),
        ]

        for system_slug, lessons in mission3_systems:
            for slug, title in lessons:
                mode = "video" if slug in video_steps else "info"
                xp_reward = 20 if mode == "video" else None
                add_step(3, slug, title, order, content_mode=mode, xp_reward=xp_reward, group_slug=system_slug)
                order += 1

        # Mission 4: Assembly steps
        order = 1
        add_step(4, "assemble-frame", "The Assembly", order, content_mode="video", xp_reward=20)
        order += 1
        add_step(4, "final-wiring", "Making Connections", order)
        order += 1
        add_step(4, "combine-code", "Combining Codes", order)

        created = 0
        updated = 0
        for data in steps:
            xp_reward = data.pop("xp_reward")
            defaults = {
                "title": data["title"],
                "order": data["order"],
                "content_mode": data["content_mode"],
                "is_quiz": data["is_quiz"],
            }
            if xp_reward is not None:
                defaults["xp_reward"] = xp_reward
            step, was_created = Step.objects.update_or_create(
                mission_number=data["mission_number"],
                group_slug=data["group_slug"],
                slug=data["slug"],
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        badges = [
            {
                "name": "Toolbox Explorer",
                "description": "Complete Mission 1 and master the tools and parts.",
                "mission_number": 1,
                "rule_type": "mission_complete",
            },
            {
                "name": "Brain Builder",
                "description": "Complete Mission 2 and power up Pedro's brain.",
                "mission_number": 2,
                "rule_type": "mission_complete",
            },
            {
                "name": "System Builder",
                "description": "Complete Mission 3 systems and build Pedro.",
                "mission_number": 3,
                "rule_type": "mission_complete",
            },
            {
                "name": "Master Assembler",
                "description": "Complete Mission 4 and finish Pedro's assembly.",
                "mission_number": 4,
                "rule_type": "mission_complete",
            },
        ]

        badge_created = 0
        badge_updated = 0
        for badge_data in badges:
            badge, was_created = Badge.objects.update_or_create(
                name=badge_data["name"],
                defaults=badge_data,
            )
            if was_created:
                badge_created += 1
            else:
                badge_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Steps seeded. Created: {created}, Updated: {updated}."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Badges seeded. Created: {badge_created}, Updated: {badge_updated}."
            )
        )
