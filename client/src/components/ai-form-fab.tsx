import { Sparkles, Loader2, CheckCircle } from "lucide-react";
import { useState } from "react";
import { Button } from "~/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "~/components/ui/dialog";
import { Textarea } from "~/components/ui/textarea";
import { useAIFillForm } from "~/lib/api/form/useForm";
import { toast } from "sonner";

interface AIFormFABProps {
  formId: string;
  onFillComplete: (responses: Record<string, any>) => void;
}

export function AIFormFAB({ formId, onFillComplete }: AIFormFABProps) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [userInput, setUserInput] = useState("");
  const { mutate: fillForm, isPending } = useAIFillForm();

  const handleSubmit = () => {
    if (!userInput.trim()) {
      toast.error("Please enter some text to describe your response");
      return;
    }

    fillForm(
      {
        formId,
        userInput: userInput.trim(),
      },
      {
        onSuccess: (data) => {
          if (data.success && data.responses) {
            onFillComplete(data.responses);
            toast.success("Form filled successfully! Please review and submit.", {
              icon: <CheckCircle className="h-4 w-4" />,
            });
            setIsDialogOpen(false);
            setUserInput("");
          } else {
            toast.error("Failed to process AI response");
          }
        },
        onError: (error: any) => {
          console.error("AI fill error:", error);
          const errorMessage =
            error.response?.data?.error ||
            "Failed to process your input. Please try again.";
          toast.error(errorMessage);
        },
      },
    );
  };

  return (
    <>
      {/* Floating Action Button */}
      <Button
        onClick={() => setIsDialogOpen(true)}
        className="group fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full shadow-lg transition-all hover:scale-110 hover:shadow-xl focus:outline-none bg-primary text-foreground"
        aria-label="AI Fill Form"
      >
        <Sparkles className="h-6 w-6 transition-transform group-hover:rotate-12" />
      </Button>

      {/* AI Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-background text-foreground">
                <Sparkles className="h-5 w-5 text-primary" />
              </div>
              <span>AI Form Assistant</span>
            </DialogTitle>
            <DialogDescription>
              Describe what you want to say in natural language, and I'll fill out the
              form for you. You can review and edit the responses before submitting.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="ai-input" className="text-sm font-medium">
                What do you want to express?
              </label>
              <Textarea
                id="ai-input"
                placeholder="Example: I'm from Habitat hostel. I'm a male vegetarian student. The food quality is good but I'd like to improve the variety and taste. I rate it 8 out of 10."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                className="min-h-[120px] resize-none"
                disabled={isPending}
              />
              <p className="text-muted-foreground text-xs">
                Be as detailed as possible to get accurate results.
              </p>
            </div>
          </div>

          <DialogFooter className="flex-col space-y-2 sm:flex-row sm:space-x-2 sm:space-y-0">
            <Button
              variant="outline"
              onClick={() => {
                setIsDialogOpen(false);
                setUserInput("");
              }}
              disabled={isPending}
              className="w-full sm:w-auto"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={!userInput.trim() || isPending}
              className="w-full bg-primary text-foreground sm:w-auto"
            >
              {isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Fill Form with AI
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

