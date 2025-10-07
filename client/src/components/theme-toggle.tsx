import { MoonIcon, SunIcon } from "lucide-react";

import { useTheme } from "~/components/theme-provider";
import { Button } from "~/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const changeTheme = () => setTheme(theme == 'light'? 'dark': 'light');

  return (
    <Button onClick={changeTheme} variant="outline" size="icon">
      {
        theme == 'light'?
        <MoonIcon className="absolute h-[1.2rem] w-[1.2rem] transition-all" />
        :
        <SunIcon className="h-[1.2rem] w-[1.2rem] transition-all" />
      }
    </Button>
  );
}
