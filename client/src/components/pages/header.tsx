import { Link } from "@tanstack/react-router";
import { ThemeToggle } from "~/components/theme-toggle";
import GetUserCode from "./get-user-code";

export default function Header() {
  return (
    <header className="bg-background border-border sticky top-0 z-50 h-16 border-b">
      <div className="container mx-auto flex h-full items-center justify-between px-4">
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="text-foreground hover:text-primary text-xl font-bold transition-colors"
          >
            AnomyForm
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <GetUserCode />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
