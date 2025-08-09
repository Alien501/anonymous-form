import { Link } from "@tanstack/react-router";
import { ThemeToggle } from "~/components/theme-toggle";

export default function Header() {
  return (
    <header className="h-16 bg-background border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-4 h-full flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link 
            to="/" 
            className="text-xl font-bold text-foreground hover:text-primary transition-colors"
          >
            AnomyForm
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}