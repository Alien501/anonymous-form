import { createFileRoute, Link } from "@tanstack/react-router";
import { ThemeToggle } from "~/components/theme-toggle";
import { Button } from "~/components/ui/button";

export const Route = createFileRoute("/")({
  component: Home,
});

function Home() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-10 p-2">
    </div>
  );
}
