import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  AlertCircle,
  CheckCircle,
  CheckSquare,
  ChevronDown,
  Circle,
  FileText,
  Hash,
  Square,
  Upload,
  User,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Checkbox } from "~/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "~/components/ui/dialog";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";
import { Textarea } from "~/components/ui/textarea";
import { useForm, useSubmitFormResponse } from "~/lib/api/form/useForm";

export const Route = createFileRoute("/form/edit/$formId/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { formId } = Route.useParams();
  const navigate = useNavigate();
  const { data: form, isLoading, error } = useForm(formId);
  const {
    mutate: submitForm,
    isPending: isSubmitting,
    error: submitError,
  } = useSubmitFormResponse();
  const [formResponses, setFormResponses] = useState<Record<string, any>>({});
  const [fileObjects, setFileObjects] = useState<Record<string, File | null>>({});
  const [fileValidationErrors, setFileValidationErrors] = useState<
    Record<string, string>
  >({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showUserCodeModal, setShowUserCodeModal] = useState(false);
  const [userCode, setUserCode] = useState("");
  const [userCodeError, setUserCodeError] = useState("");

  // Get questions safely - will be empty array if form is undefined
  const questions =
    form?.form_questions?.sort((a, b) => a.form_index - b.form_index) || [];

  // Function to validate file sizes
  const validateFileSize = (file: File, minSize: number, maxSize: number): boolean => {
    const fileSizeMB = file.size / (1024 * 1024);

    if (minSize > 0 && fileSizeMB < minSize) {
      return false;
    }

    if (maxSize > 0 && fileSizeMB > maxSize) {
      return false;
    }

    return true;
  };

  // Function to get file validation error message
  const getFileValidationError = (
    file: File,
    minSize: number,
    maxSize: number,
  ): string | null => {
    const fileSizeMB = file.size / (1024 * 1024);

    if (minSize > 0 && fileSizeMB < minSize) {
      return `File size must be at least ${minSize} MB`;
    }

    if (maxSize > 0 && fileSizeMB > maxSize) {
      return `File size must be less than ${maxSize} MB`;
    }

    return null;
  };

  // Real-time file validation - now called unconditionally
  useEffect(() => {
    const newValidationErrors: Record<string, string> = {};

    questions.forEach((formQuestion) => {
      const question = formQuestion.question;
      const fileObject = fileObjects[question.id];

      if (fileObject && question.answer_type === "file") {
        const error = getFileValidationError(
          fileObject,
          question.min_len,
          question.max_len,
        );
        if (error) {
          newValidationErrors[question.id] = error;
        }
      }
    });

    setFileValidationErrors(newValidationErrors);
  }, [fileObjects, form?.form_questions]);

  // Early returns after all hooks
  if (!formId) {
    navigate({ to: "/" });
    return null;
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="border-primary mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2"></div>
          <p className="text-muted-foreground">Loading your form...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center text-red-500">
          <AlertCircle className="mx-auto mb-4 h-12 w-12" />
          <h2 className="mb-2 text-xl font-semibold">Error loading form</h2>
          <p className="text-muted-foreground">{error.message}</p>
        </div>
      </div>
    );
  }

  if (!form) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-muted-foreground text-center">
          <FileText className="mx-auto mb-4 h-16 w-16" />
          <h2 className="mb-2 text-xl font-semibold">Form not found</h2>
          <p>The form you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  // Check if all required questions are filled out and file sizes are valid
  const isFormValid = questions.every((formQuestion) => {
    const question = formQuestion.question;
    if (!question.required) return true; // Non-required questions are always valid

    const value = formResponses[formQuestion.question.id];

    if (question.answer_type === "file") {
      if (value === null || value === undefined) {
        return !question.required; // If not required, it's valid to have no file
      }

      // Check if we have a file object and validate its size
      const fileObject = fileObjects[formQuestion.question.id];
      if (fileObject) {
        return validateFileSize(fileObject, question.min_len, question.max_len);
      }

      return false; // No file object found
    } else if (question.answer_type === "checkbox") {
      return Array.isArray(value) && value.length > 0;
    } else if (question.answer_type === "boolean") {
      return value === true || value === false; // Both true and false are valid
    } else {
      return value !== null && value !== undefined && value !== "";
    }
  });

  // Calculate progress for required questions
  const requiredQuestions = questions.filter((q) => q.question.required);
  const completedRequiredQuestions = requiredQuestions.filter((formQuestion) => {
    const question = formQuestion.question;
    const value = formResponses[question.id];

    if (question.answer_type === "file") {
      if (value === null || value === undefined) {
        return false;
      }

      // Check if we have a file object and validate its size
      const fileObject = fileObjects[question.id];
      if (fileObject) {
        return validateFileSize(fileObject, question.min_len, question.max_len);
      }

      return false; // No file object found
    } else if (question.answer_type === "checkbox") {
      return Array.isArray(value) && value.length > 0;
    } else if (question.answer_type === "boolean") {
      return value === true || value === false;
    } else {
      return value !== null && value !== undefined && value !== "";
    }
  }).length;

  const progressPercentage =
    requiredQuestions.length > 0
      ? (completedRequiredQuestions / requiredQuestions.length) * 100
      : 100;

  const handleSubmit = () => {
    if (!isFormValid) return;

    // Show user code modal
    setShowUserCodeModal(true);
  };

  const handleUserCodeSubmit = () => {
    if (!userCode.trim()) {
      setUserCodeError("User code is required");
      return;
    }

    setUserCodeError("");

    const formData = new FormData();
    formData.append("user_code", userCode.trim());
    formData.append("formId", form.id);

    // Process responses and handle file uploads
    const responses: Record<string, any> = {};

    // Validate that required file fields have actual files
    for (const formQuestion of questions) {
      const questionId = formQuestion.question.id;
      const question = formQuestion.question;
      const value = formResponses[questionId];

      if (question.answer_type === "file" && question.required) {
        const fileObject = fileObjects[questionId];
        if (!fileObject) {
          setUserCodeError(`File upload is required for: ${question.question}`);
          return;
        }
      }
    }

    questions.forEach((formQuestion) => {
      const questionId = formQuestion.question.id;
      const question = formQuestion.question;
      const value = formResponses[questionId];

      if (
        question.answer_type === "file" &&
        value &&
        typeof value === "object" &&
        "name" in value
      ) {
        // This is a file field
        responses[questionId] = {
          question: question.question,
          answer_type: question.answer_type,
          value: {
            name: value.name,
            size: value.size,
            type: value.type,
            lastModified: value.lastModified,
          },
          required: question.required,
        };

        // Append the actual file if it exists
        const fileObject = fileObjects[questionId];
        if (fileObject) {
          formData.append(`file_${questionId}`, fileObject);
        }
      } else {
        responses[questionId] = {
          question: question.question,
          answer_type: question.answer_type,
          value: value || null,
          required: question.required,
        };
      }
    });

    formData.append("responses", JSON.stringify(responses));

    submitForm(formData, {
      onSuccess: (data) => {
        setIsSubmitted(true);
        setShowUserCodeModal(false);
        setUserCode("");
        setIsSubmitted(false);
        setFormResponses({});
        setFileObjects({});
        setFileValidationErrors({});
      },
      onError: (error: any) => {
        console.error("Form submission failed:", error);
        if (error.response?.data?.message) {
          setUserCodeError(error.response.data.message);
        } else {
          setUserCodeError("An error occurred while submitting the form");
        }
      },
    });
  };

  return (
    <div className="bg-background min-h-screen">
      {/* Form Header */}
      <div className="px-4 py-12 text-center">
        <h1 className="text-foreground mb-3 text-3xl font-bold md:text-4xl">
          {form.name}
        </h1>
        <p className="text-muted-foreground mx-auto max-w-2xl text-base">
          Please fill out the form below. All required fields are marked with an asterisk
          (*).
        </p>
      </div>

      {/* Questions Container */}
      <div className="mx-auto max-w-2xl px-4 pb-12">
        {questions.length > 0 ? (
          <div className="space-y-6">
            {questions.map((question, index) => (
              <QuestionRenderer
                key={question.id}
                question={question.question}
                index={index + 1}
                total={questions.length}
                onValueChange={(questionId, value) => {
                  setFormResponses((prev) => ({
                    ...prev,
                    [questionId]: value,
                  }));
                }}
                onFileChange={(questionId: string, file: File | null) => {
                  setFileObjects((prev) => ({
                    ...prev,
                    [questionId]: file,
                  }));
                }}
                onFileValidationError={(questionId: string, error: string | null) => {
                  setFileValidationErrors((prev) => ({
                    ...prev,
                    [questionId]: error || "",
                  }));
                }}
                fileValidationError={fileValidationErrors[question.question.id]}
              />
            ))}

            {/* Submit Button */}
            <div className="pt-6 text-center">
              {isSubmitted ? (
                <div className="text-center">
                  <div className="mb-4 inline-flex items-center space-x-2 text-green-600">
                    <CheckCircle className="h-5 w-5" />
                    <span className="font-medium">Form submitted successfully!</span>
                  </div>
                  <p className="text-muted-foreground text-sm">
                    Your response has been recorded.
                  </p>
                </div>
              ) : (
                <>
                  {/* Progress Indicator */}
                  {requiredQuestions.length > 0 && (
                    <div className="mb-4 text-center">
                      <div className="mb-2 flex items-center justify-center space-x-2">
                        <span className="text-muted-foreground text-sm">
                          Required questions completed:
                        </span>
                        <span className="text-sm font-medium">
                          {completedRequiredQuestions} / {requiredQuestions.length}
                        </span>
                      </div>
                      <div className="bg-muted mx-auto h-2 w-full max-w-xs rounded-full">
                        <div
                          className="bg-primary h-2 rounded-full transition-all duration-300 ease-in-out"
                          style={{ width: `${progressPercentage}%` }}
                        ></div>
                      </div>
                    </div>
                  )}

                  <Button
                    size="default"
                    className="px-6 py-2"
                    onClick={handleSubmit}
                    disabled={
                      !isFormValid ||
                      isSubmitting ||
                      Object.keys(fileValidationErrors).length != 0
                    }
                  >
                    {isSubmitting ? "Submitting..." : "Submit Form"}
                  </Button>

                  {!isFormValid && requiredQuestions.length > 0 && (
                    <p className="text-muted-foreground mt-2 text-xs">
                      Please complete all required questions to submit
                    </p>
                  )}

                  {/* File validation errors */}
                  {Object.keys(fileValidationErrors).length > 0 && (
                    <div className="mt-2 text-center">
                      <p className="mb-1 text-sm font-medium text-red-500">
                        Please fix the following file upload issues:
                      </p>
                      {Object.entries(fileValidationErrors).map(([questionId, error]) => {
                        if (!error) return null;
                        const question = questions.find(
                          (q) => q.question.id === questionId,
                        );
                        return (
                          <p key={questionId} className="text-xs text-red-500">
                            • {question?.question.question}: {error}
                          </p>
                        );
                      })}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        ) : (
          <div className="py-12 text-center">
            <FileText className="text-muted-foreground mx-auto mb-3 h-12 w-12" />
            <h2 className="mb-2 text-xl font-semibold">This form is empty</h2>
            <p className="text-muted-foreground">No questions have been added yet.</p>
          </div>
        )}
      </div>

      {/* User Code Modal */}
      <Dialog
        open={showUserCodeModal}
        onOpenChange={(open) => {
          setShowUserCodeModal(open);
          if (!open) {
            setUserCode("");
            setUserCodeError("");
            setFileValidationErrors({}); // Clear file validation errors when dialog closes
          }
        }}
      >
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <User className="h-5 w-5" />
              <span>Enter Your User Code</span>
            </DialogTitle>
            <DialogDescription>
              Please enter your unique user code to submit this form. This helps us
              prevent duplicate submissions.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="user-code">User Code</Label>
              <Input
                id="user-code"
                type="text"
                placeholder="Enter your 6-digit user code"
                value={userCode}
                onChange={(e) => {
                  setUserCode(e.target.value.toUpperCase());
                  if (userCodeError) setUserCodeError("");
                }}
                className="text-center font-mono text-lg tracking-widest"
                maxLength={6}
                autoFocus
              />
              {userCodeError && (
                <div className="flex items-center space-x-2 text-sm text-red-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>{userCodeError}</span>
                </div>
              )}
            </div>
          </div>

          <DialogFooter className="flex-col space-y-2 sm:flex-row sm:space-y-0">
            <Button
              variant="outline"
              onClick={() => {
                setShowUserCodeModal(false);
                setUserCode("");
                setUserCodeError("");
                setFileValidationErrors({}); // Clear file validation errors when canceling
              }}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              onClick={handleUserCodeSubmit}
              disabled={!userCode.trim() || isSubmitting}
            >
              {isSubmitting ? "Submitting..." : "Submit Form"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

interface QuestionRendererProps {
  question: {
    id: string;
    question: string;
    required: boolean;
    answer_type: string;
    min_len: number;
    max_len: number;
    options: string;
    file_type: string;
  };
  index: number;
  total: number;
  onValueChange: (
    questionId: string,
    value:
      | string
      | number
      | boolean
      | string[]
      | { name: string; size: number; type: string; lastModified: number }
      | null,
  ) => void;
  onFileChange: (questionId: string, file: File | null) => void;
  onFileValidationError: (questionId: string, error: string | null) => void;
  fileValidationError?: string;
}

function QuestionRenderer({
  question,
  index,
  total,
  onValueChange,
  onFileChange,
  onFileValidationError,
  fileValidationError,
}: QuestionRendererProps) {
  const [value, setValue] = useState<string | number | boolean | string[]>("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string>("");

  const validateInput = (input: string | number | boolean | string[]) => {
    if (question.required) {
      if (typeof input === "boolean") {
        // For boolean fields, both true and false are valid values
        if (input === undefined || input === null) {
          setError("This field is required");
          return false;
        }
      } else if (typeof input === "string") {
        if (!input || input.trim() === "") {
          setError("This field is required");
          return false;
        }
      } else if (typeof input === "number") {
        if (input === undefined || input === null) {
          setError("This field is required");
          return false;
        }
      } else if (Array.isArray(input)) {
        if (input.length === 0) {
          setError("This field is required");
          return false;
        }
      } else if (input === undefined || input === null) {
        setError("This field is required");
        return false;
      }
    }

    // Only apply text length validation for text inputs, not for file uploads
    if (
      question.answer_type === "text" &&
      typeof input === "string" &&
      input.trim() !== ""
    ) {
      if (question.min_len > 0 && input.length < question.min_len) {
        setError(`Minimum ${question.min_len} characters required`);
        return false;
      }
      if (question.max_len > 0 && input.length > question.max_len) {
        setError(`Maximum ${question.max_len} characters allowed`);
        return false;
      }
    }

    setError("");
    return true;
  };

  const handleInputChange = (newValue: string | number | boolean | string[]) => {
    setValue(newValue);
    validateInput(newValue);
    onValueChange(question.id, newValue);
  };

  const getQuestionIcon = () => {
    switch (question.answer_type) {
      case "text":
        return <FileText className="h-5 w-5" />;
      case "number":
        return <Hash className="h-5 w-5" />;
      case "boolean":
        return <CheckSquare className="h-5 w-5" />;
      case "radio":
        return <Circle className="h-5 w-5" />;
      case "checkbox":
        return <Square className="h-5 w-5" />;
      case "select":
        return <ChevronDown className="h-5 w-5" />;
      case "file":
        return <Upload className="h-5 w-5" />;
      default:
        return <FileText className="h-5 w-5" />;
    }
  };

  const getFileTypeDescription = (mimeType: string) => {
    switch (mimeType) {
      case "image/*":
        return "Images (jpg, png, gif, etc.)";
      case "application/pdf":
        return "PDF files";
      case "application/msword":
        return "Word documents (.doc)";
      case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return "Word documents (.docx)";
      case "text/csv":
        return "CSV files";
      case "text/plain":
        return "Text files (.txt)";
      case "application/vnd.ms-excel":
        return "Excel files (.xls)";
      case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return "Excel files (.xlsx)";
      case "application/zip":
        return "ZIP archives";
      case "*/*":
        return "All file types";
      default:
        return mimeType;
    }
  };

  const renderInput = () => {
    switch (question.answer_type) {
      case "text": {
        return (
          <Textarea
            placeholder="Type your answer here"
            value={value as string}
            onChange={(e) => handleInputChange(e.target.value)}
            className="focus:border-primary border-2 px-3 py-2"
            maxLength={question.max_len > 0 ? question.max_len : undefined}
          />
        );
      }

      case "number": {
        return (
          <Input
            type="number"
            placeholder="Enter a number..."
            value={value as number}
            onChange={(e) => handleInputChange(parseInt(e.target.value) || "")}
            className="focus:border-primary border-2 px-3 py-2"
          />
        );
      }

      case "boolean": {
        return (
          <div className="flex space-x-3">
            <Button
              variant={value === true ? "default" : "outline"}
              onClick={() => handleInputChange(true)}
              className="flex-1 py-2"
            >
              Yes
            </Button>
            <Button
              variant={value === false ? "default" : "outline"}
              onClick={() => handleInputChange(false)}
              className="flex-1 py-2"
            >
              No
            </Button>
          </div>
        );
      }

      case "radio": {
        const radioOptions = question.options ? question.options.split("||") : [];
        return (
          <RadioGroup
            value={value as string}
            onValueChange={(newValue) => handleInputChange(newValue)}
            className="space-y-2"
          >
            {radioOptions.map((option) => (
              <div key={option} className="flex items-center space-x-2">
                <RadioGroupItem value={option} id={`radio-${question.id}-${option}`} />
                <Label
                  htmlFor={`radio-${question.id}-${option}`}
                  className="cursor-pointer text-sm"
                >
                  {option}
                </Label>
              </div>
            ))}
          </RadioGroup>
        );
      }

      case "checkbox": {
        const checkboxOptions = question.options ? question.options.split("||") : [];
        return (
          <div className="space-y-2">
            {checkboxOptions.map((option) => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`checkbox-${question.id}-${option}`}
                  checked={(value as string[])?.includes(option) || false}
                  onCheckedChange={(checked) => {
                    const currentValues = (value as string[]) || [];
                    if (checked) {
                      handleInputChange([...currentValues, option]);
                    } else {
                      handleInputChange(currentValues.filter((v) => v !== option));
                    }
                  }}
                />
                <Label
                  htmlFor={`checkbox-${question.id}-${option}`}
                  className="cursor-pointer text-sm"
                >
                  {option}
                </Label>
              </div>
            ))}
          </div>
        );
      }

      case "select": {
        const selectOptions = question.options ? question.options.split("||") : [];
        return (
          <Select
            value={value as string}
            onValueChange={(newValue) => handleInputChange(newValue)}
          >
            <SelectTrigger className="border-muted-foreground/10 focus:border-primary w-full border-2 px-3 py-2">
              <SelectValue placeholder="Select an option..." />
            </SelectTrigger>
            <SelectContent>
              {selectOptions.map((option) => (
                <SelectItem key={option} value={option}>
                  {option}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );
      }

      case "file": {
        return (
          <div className="space-y-3">
            <div className="border-muted-foreground hover:border-primary cursor-pointer rounded-lg border-2 border-dashed p-6 text-center transition-colors">
              <input
                type="file"
                accept={question.file_type !== "none" ? question.file_type : undefined}
                onChange={(e) => {
                  const selectedFile = e.target.files?.[0];
                  if (selectedFile) {
                    setFile(selectedFile);
                    // For file uploads, validate file size in MB
                    const fileSizeMB = selectedFile.size / (1024 * 1024);

                    if (question.required && !selectedFile) {
                      setError("This field is required");
                      onFileValidationError(question.id, "This field is required");
                    } else if (question.min_len > 0 && fileSizeMB < question.min_len) {
                      setError(`File size must be at least ${question.min_len} MB`);
                      onFileValidationError(
                        question.id,
                        `File size must be at least ${question.min_len} MB`,
                      );
                    } else if (question.max_len > 0 && fileSizeMB > question.max_len) {
                      setError(`File size must be less than ${question.max_len} MB`);
                      onFileValidationError(
                        question.id,
                        `File size must be less than ${question.max_len} MB`,
                      );
                    } else {
                      setError("");
                      onFileValidationError(question.id, null);
                      // Call onValueChange with file information
                      onValueChange(question.id, {
                        name: selectedFile.name,
                        size: selectedFile.size,
                        type: selectedFile.type,
                        lastModified: selectedFile.lastModified,
                      });
                      onFileChange(question.id, selectedFile);
                    }
                  } else {
                    onFileChange(question.id, null);
                    onFileValidationError(question.id, null);
                  }
                }}
                className="sr-only"
                id={`file-${question.id}`}
              />
              <label htmlFor={`file-${question.id}`} className="cursor-pointer">
                <Upload className="text-muted-foreground mx-auto mb-3 h-8 w-8" />
                <p className="mb-1 text-sm font-medium">Click to upload a file</p>
                <p className="text-muted-foreground text-xs">
                  {question.file_type !== "none" && question.file_type !== "*/*"
                    ? `Accepted: ${getFileTypeDescription(question.file_type)}`
                    : "All file types accepted"}
                </p>
                {(question.min_len > 0 || question.max_len > 0) && (
                  <p className="text-muted-foreground mt-1 text-xs">
                    Size: {question.min_len > 0 ? `${question.min_len} MB` : "0 MB"} -{" "}
                    {question.max_len > 0 ? `${question.max_len} MB` : "Unlimited"}
                  </p>
                )}
              </label>
            </div>
            {file && (
              <div className="bg-muted flex items-center space-x-2 rounded-lg p-2">
                <FileText className="text-primary h-4 w-4" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium">{file.name}</p>
                  <p className="text-muted-foreground text-xs">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setFile(null);
                    onValueChange(question.id, null);
                    onFileChange(question.id, null);
                    onFileValidationError(question.id, null);
                    if (question.required) {
                      setError("This field is required");
                    } else {
                      setError("");
                    }
                  }}
                >
                  Remove
                </Button>
              </div>
            )}
            {/* {fileValidationError && (
              <div className="flex items-center space-x-2 text-sm text-red-500">
                <AlertCircle className="h-4 w-4" />
                <span>{fileValidationError}</span>
              </div>
            )} */}
          </div>
        );
      }

      default:
        return <Input placeholder="Unsupported question type" disabled />;
    }
  };

  return (
    <Card className="shadow-accent/10 rounded-md shadow-none transition-shadow hover:shadow-xl">
      <CardHeader>
        <div className="flex items-center space-x-3">
          <div className="bg-primary/10 text-primary flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full">
            {getQuestionIcon()}
          </div>
          <div className="flex-1">
            <div className="mb-0 flex items-center space-x-2">
              <span className="text-muted-foreground bg-background/20 rounded-md px-1 py-0.5 text-xs font-medium">
                Question {index} of {total}
              </span>
              {question.required && (
                <span className="text-xs font-medium text-red-500">*</span>
              )}
            </div>
            <CardTitle className="text-lg leading-relaxed">{question.question}</CardTitle>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Input Field */}
        {renderInput()}

        {/* Error Message */}
        {error && (
          <div className="flex items-center space-x-2 text-sm text-red-500">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        {/* Character Count for Text Inputs */}
        {question.answer_type === "text" && question.max_len > 0 && (
          <div className="text-muted-foreground text-right text-xs">
            {(value as string)?.length || 0} / {question.max_len} characters
          </div>
        )}
      </CardContent>
    </Card>
  );
}
