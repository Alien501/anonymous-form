import { createFileRoute } from "@tanstack/react-router";
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  FileText,
  Lock,
  Settings,
  Shield,
  Upload,
  Users,
  Zap,
} from "lucide-react";
import { Badge } from "~/components/ui/badge";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";

export const Route = createFileRoute("/")({
  component: Home,
});

function Home() {
  const features = [
    {
      title: "Complete Anonymity",
      desc: "Ensure respondent privacy with fully anonymous submissions. No personal data is ever collected or stored.",
      icon: <Lock className="h-6 w-6" />,
    },
    {
      title: "Smart Access Control",
      desc: "Restrict form access by roles, departments, and groups. Control exactly who can respond to your forms.",
      icon: <Shield className="h-6 w-6" />,
    },
    {
      title: "Unique Verification Codes",
      desc: "Each user gets a unique 6-character code to prevent multiple submissions while maintaining anonymity.",
      icon: <CheckCircle2 className="h-6 w-6" />,
    },
    {
      title: "Rich Question Types",
      desc: "Support for text, numbers, boolean, radio, checkbox, select, and file uploads with size controls.",
      icon: <FileText className="h-6 w-6" />,
    },
    {
      title: "File Upload Support",
      desc: "Accept various file types including images, PDFs, documents, spreadsheets, and more with size limits.",
      icon: <Upload className="h-6 w-6" />,
    },
    {
      title: "No Sign-in Required",
      desc: "Users can submit forms anonymously using just their unique code. No account creation needed.",
      icon: <Zap className="h-6 w-6" />,
    },
  ];

  const questionTypes = [
    { name: "Text", desc: "Long and short text responses" },
    { name: "Number", desc: "Numeric inputs with validation" },
    { name: "Boolean", desc: "Yes/No questions" },
    { name: "Radio", desc: "Single choice from options" },
    { name: "Checkbox", desc: "Multiple choice selections" },
    { name: "Select", desc: "Dropdown selections" },
    { name: "File Upload", desc: "Document and media uploads" },
  ];

  const fileTypes = [
    "Images (JPG, PNG, GIF)",
    "PDF Documents",
    "Word Documents (.doc, .docx)",
    "Excel Spreadsheets (.xls, .xlsx)",
    "CSV Files",
    "Text Files (.txt)",
    "ZIP Archives",
  ];

  return (
    <div className="bg-background text-foreground">
      {/* Hero Section */}
      <section className="h-[calc(min-h-screen, 140px)] flex flex-col items-center justify-center px-4 py-20 text-center">
        <div className="mx-auto max-w-4xl">
          <Badge className="bg-primary/10 text-primary border-primary/20 mb-8">
            Secure • Anonymous • Professional
          </Badge>

          <h1 className="mb-8 text-6xl font-bold tracking-tight md:text-7xl">
            AnomyForm
          </h1>

          <p className="text-muted-foreground mx-auto mb-12 max-w-2xl text-xl md:text-2xl">
            Create secure, anonymous forms for your organization. Get honest feedback
            while maintaining complete privacy.
          </p>

          <div className="flex flex-col justify-center gap-4 sm:flex-row">
            <Button size="lg" className="px-8 py-3">
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="relative px-8 py-3">
              <a href="#features" className="absolute inset-0" />
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="px-4 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-16 text-center">
            <h2 className="mb-6 text-4xl font-bold tracking-tight">
              Why Organizations Choose AnomyForm
            </h2>
            <p className="text-muted-foreground mx-auto max-w-2xl text-lg">
              Built for organizations that value privacy and need honest feedback
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, idx) => (
              <Card
                key={idx}
                className="border shadow-sm transition-shadow hover:shadow-md"
              >
                <CardHeader>
                  <div className="bg-primary/10 text-primary mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground leading-relaxed">{feature.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-muted/30 px-4 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-16 text-center">
            <h2 className="mb-6 text-4xl font-bold tracking-tight">How It Works</h2>
            <p className="text-muted-foreground mx-auto max-w-2xl text-lg">
              Simple three-step process to get anonymous feedback
            </p>
          </div>

          <div className="grid gap-12 md:grid-cols-3">
            {[
              {
                step: "1",
                title: "Create Your Form",
                desc: "Design your form with various question types, set access controls, and configure submission rules.",
                icon: <Settings className="h-8 w-8" />,
              },
              {
                step: "2",
                title: "Share with Users",
                desc: "Distribute unique codes to your target audience. No sign-in required - just the code.",
                icon: <Users className="h-8 w-8" />,
              },
              {
                step: "3",
                title: "Collect Responses",
                desc: "Receive anonymous submissions while maintaining complete privacy and preventing duplicates.",
                icon: <BarChart3 className="h-8 w-8" />,
              },
            ].map((item, idx) => (
              <div
                key={idx}
                className="bg-card rounded-md p-2 text-center hover:shadow-sm"
              >
                <div className="mb-8 flex justify-center">
                  <div className="bg-primary/10 text-primary flex h-16 w-16 items-center justify-center rounded-full">
                    {item.icon}
                  </div>
                </div>

                <div className="mb-4">
                  <Badge variant="outline" className="text-sm">
                    Step {item.step}
                  </Badge>
                </div>
                <h3 className="mb-4 text-xl font-semibold">{item.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Question Types */}
      <section className="px-4 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-16 text-center">
            <h2 className="mb-6 text-4xl font-bold tracking-tight">
              Flexible Question Types
            </h2>
            <p className="text-muted-foreground mx-auto max-w-2xl text-lg">
              Support for all common question formats with validation
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {questionTypes.map((type, idx) => (
              <Card
                key={idx}
                className="border text-center shadow-sm transition-shadow hover:shadow-md"
              >
                <CardContent className="pt-6">
                  <h3 className="mb-2 font-semibold">{type.name}</h3>
                  <p className="text-muted-foreground text-sm">{type.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* File Upload Support */}
      <section className="bg-muted/30 px-4 py-24">
        <div className="mx-auto max-w-4xl">
          <div className="mb-16 text-center">
            <h2 className="mb-6 text-4xl font-bold tracking-tight">
              File Upload Support
            </h2>
            <p className="text-muted-foreground mx-auto max-w-2xl text-lg">
              Accept various file types with size controls and validation
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {fileTypes.map((type, idx) => (
              <div
                key={idx}
                className="bg-background flex items-center rounded-lg border p-4 shadow-sm"
              >
                <CheckCircle2 className="mr-3 h-5 w-5 flex-shrink-0 text-green-600" />
                <span className="text-sm font-medium">{type}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="bg-primary text-primary-foreground px-4 py-24">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="mb-6 text-4xl font-bold tracking-tight">
            Ready to Get Honest Feedback?
          </h2>
          <p className="text-primary-foreground/90 mx-auto mb-12 max-w-2xl text-xl">
            Start creating anonymous forms today and get the insights your organization
            needs.
          </p>
          <Button size="lg" variant="secondary" className="px-8 py-3">
            Get Started Now
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t px-4 py-12">
        <div className="mx-auto max-w-4xl text-center">
          <p className="text-muted-foreground mb-2 text-sm">
            © {new Date().getFullYear()} AnomyForm. Secure anonymous forms for
            organizations.
          </p>
          <p className="text-muted-foreground/70 text-xs">
            Built with privacy and security in mind
          </p>
        </div>
      </footer>
    </div>
  );
}
