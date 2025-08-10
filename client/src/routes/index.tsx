import { createFileRoute } from "@tanstack/react-router";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Badge } from "~/components/ui/badge";
import { CheckCircle2, Lock, Users, KeyRound } from "lucide-react";

export const Route = createFileRoute("/")({
  component: Home,
});

function Home() {
  const features = [
    {
      title: "Anonymous Forms",
      desc: "Ensure respondent privacy with fully anonymous submissions.",
      icon: <Lock className="w-10 h-10 text-blue-500" />,
    },
    {
      title: "Role-Based Control",
      desc: "Restrict access and manage permissions based on user roles.",
      icon: <Users className="w-10 h-10 text-green-500" />,
    },
    {
      title: "Group Restrictions",
      desc: "Target specific groups to control who can respond.",
      icon: <CheckCircle2 className="w-10 h-10 text-purple-500" />,
    },
    {
      title: "Unique Confirmation Codes",
      desc: "Prevent multiple submissions with unique user confirmation codes.",
      icon: <KeyRound className="w-10 h-10 text-orange-500" />,
    },
  ];

  const plans = [
    {
      name: "Free",
      price: "$0",
      features: ["1 Form", "Basic Controls", "Email Support"],
    },
    {
      name: "Pro",
      price: "$19/mo",
      features: [
        "Unlimited Forms",
        "Role Restrictions",
        "Group Controls",
        "Priority Support",
      ],
    },
    {
      name: "Enterprise",
      price: "Contact Us",
      features: [
        "Custom Integrations",
        "Advanced Security",
        "Dedicated Manager",
      ],
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center flex-1 text-center px-4 py-20 bg-gradient-to-b from-blue-600 to-blue-400 text-white overflow-hidden">
        <h1 className="text-5xl md:text-6xl font-bold mb-4 drop-shadow-lg">
          AnomyForm
        </h1>
        <p className="text-lg md:text-xl max-w-2xl mb-6 opacity-90">
          Create secure, anonymous forms for your organization with smart
          access controls and unique submission verification.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Button size="lg" variant="secondary">
            Get Started
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="bg-white/10 text-white border-white/30"
          >
            Learn More
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-16 bg-background">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose Us?</h2>
        <div className="grid md:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {features.map((f, idx) => (
            <Card
              key={idx}
              className="hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
            >
              <CardHeader>
                {f.icon}
                <CardTitle className="mt-2">{f.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground">
                {f.desc}
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="px-4 py-16 bg-muted/30">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto text-center">
          {["Create Your Form", "Share with Audience", "Collect Secure Responses"].map(
            (step, idx) => (
              <div
                key={idx}
                className="p-4 rounded-lg hover:bg-muted transition-colors duration-300"
              >
                <Badge className="mb-2">Step {idx + 1}</Badge>
                <h3 className="font-semibold mb-2">{step}</h3>
                <p className="text-muted-foreground">
                  {idx === 0 &&
                    "Set up an anonymous form with custom fields and controls."}
                  {idx === 1 &&
                    "Send the form link to your organization or target groups."}
                  {idx === 2 &&
                    "Users submit anonymously and confirm with their unique code."}
                </p>
              </div>
            )
          )}
        </div>
      </section>

      {/* Pricing */}
      <section className="px-4 py-16 bg-background">
        <h2 className="text-3xl font-bold text-center mb-12">Pricing</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, idx) => (
            <Card
              key={idx}
              className="backdrop-blur-md bg-white/80 dark:bg-black/40 shadow-lg hover:scale-105 transition-all"
            >
              <CardHeader>
                <CardTitle>{plan.name}</CardTitle>
                <p className="text-2xl font-bold">{plan.price}</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-500" /> {f}
                    </li>
                  ))}
                </ul>
              </CardContent>
              <div className="p-4">
                <Button className="w-full">Choose {plan.name}</Button>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-4 py-16 bg-gradient-to-b from-blue-500 to-blue-700 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">
          Ready to Create Your First Anonymous Form?
        </h2>
        <p className="text-white/90 mb-6">
          Start today and get secure, private feedback instantly.
        </p>
        <Button size="lg" variant="secondary">
          Get Started Now
        </Button>
      </section>

      {/* Footer */}
      <footer className="px-4 py-6 bg-background border-t text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} AnomyForm. All rights reserved.
      </footer>
    </div>
  );
}
