from database_manager import DatabaseManager as dm


class DatabaseApp:

    COMANDS_DICT = {
        "SET": {
            "func": dm.apply_to_active_transaction_or_db,
            "metod": "set_value",
            "limitation": 2,
            "message": "Usage: SET <key> <value>",
        },
        "GET": {
            "func": dm.get_from_active_transaction_or_db,
            "metod": "get_value",
            "limitation": 1,
            "message": "Usage: GET <key>",
        },
        "UNSET": {
            "func": dm.apply_to_active_transaction_or_db,
            "metod": "unset_value",
            "limitation": 1,
            "message": "Usage: UNSET <key>",
        },
        "COUNTS": {
            "func": dm.get_from_active_transaction_or_db,
            "metod": "get_counter",
            "limitation": 1,
            "message": "Usage: COUNTS <value>",
        },
        "FIND": {
            "func": dm.get_from_active_transaction_or_db,
            "metod": "get_keys",
            "limitation": 1,
            "message": "Usage: FIND <key>",
        },
        "BEGIN": {
            "func": dm.begin_transaction,
            "limitation": 0,
            "message": "Usage: BEGIN",
        },
        "ROLLBACK": {
            "func": dm.rollback_transaction,
            "limitation": 0,
            "message": "Usage: ROLLBACK",
        },
        "COMMIT": {
            "func": dm.commit_transaction,
            "limitation": 0,
            "message": "Usage: COMMIT",
        },
    }

    def execute_command(self, command: str) -> None:
        try:
            cmd, args = self._split_line(command)
        except TypeError:
            return
        cmd_params = self.COMANDS_DICT.get(cmd)

        if not cmd_params:
            print(f"Unknown command: {cmd}")
            return

        if not args:
            cmd_params["func"]()
            return

        if len(args) != cmd_params["limitation"]:
            print(cmd_params["message"])
            return
        try:
            if len(args) == 2:
                cmd_params["func"](cmd_params["metod"], args[0], int(args[1]))
            else:
                arg = args[0]
                result = cmd_params["func"](
                    cmd_params["metod"], arg if arg.isalpha() else int(arg)
                )
                if result is not None:
                    print(result)
        except ValueError:
            print("Value must be number")

    @staticmethod
    def _split_line(line: str) -> tuple[str, list]:
        parts = line.split()
        if not parts:
            return
        cmd = parts[0].upper()
        args = parts[1:]
        return cmd, args if args else None

    def run(self):
        print("Welcome to the Database App. Enter commands (END or ctrl+C to exit).")
        try:
            while True:
                try:
                    command_line = input("> ").strip()
                except EOFError:
                    print("\nExiting...")
                    break

                if command_line == "END":
                    break

                self.execute_command(command_line)

        except KeyboardInterrupt:
            print("\nExiting...")


if __name__ == "__main__":
    app = DatabaseApp()
    app.run()
