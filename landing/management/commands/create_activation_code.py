from django.core.management.base import BaseCommand, CommandError

from landing.models import ActivationCode, normalize_activation_code


class Command(BaseCommand):
    help = "Create an activation code and choose whether it is temporary or permanent."

    def add_arguments(self, parser):
        parser.add_argument("code", help="Activation code to create.")
        parser.add_argument(
            "--type",
            choices=[ActivationCode.TYPE_TEMPORARY, ActivationCode.TYPE_PERMANENT],
            dest="code_type",
            help="Activation code type. If omitted, you will be prompted.",
        )

    def _prompt_for_code_type(self) -> str:
        prompt = "Create this activation code as temporary or permanent? [temporary/permanent]: "
        while True:
            self.stdout.write(prompt, ending="")
            response = self.stdin.readline().strip().lower()
            if response in {ActivationCode.TYPE_TEMPORARY, ActivationCode.TYPE_PERMANENT}:
                return response
            self.stdout.write("Enter 'temporary' or 'permanent'.")

    def handle(self, *args, **options):
        raw_code = options["code"]
        code = normalize_activation_code(raw_code)
        if not code:
            raise CommandError("Activation code cannot be empty.")

        code_type = options.get("code_type")
        if not code_type:
            if not self.stdin.isatty():
                raise CommandError(
                    "You must pass --type temporary|permanent when running non-interactively."
                )
            code_type = self._prompt_for_code_type()

        activation_code, created = ActivationCode.objects.get_or_create(code=code)
        activation_code.set_code_type(code_type)
        activation_code.save(update_fields=["is_reusable"])

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} activation code {activation_code.code} as {activation_code.get_code_type_label().lower()}."
            )
        )
