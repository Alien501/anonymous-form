import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Checkbox } from "~/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "~/components/ui/select";
import { Label } from "~/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "~/components/ui/dialog";
import { useForm, useSubmitFormResponse } from "~/lib/api/form/useForm";
import { useState } from "react";
import { 
  FileText, 
  Hash, 
  CheckSquare, 
  Circle, 
  Square, 
  ChevronDown, 
  Upload,
  AlertCircle,
  CheckCircle,
  User
} from "lucide-react";
import { Textarea } from "~/components/ui/textarea";

export const Route = createFileRoute("/form/edit/$formId/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { formId } = Route.useParams();
  const navigate = useNavigate();
  const { data: form, isLoading, error } = useForm(formId);
  const { mutate: submitForm, isPending: isSubmitting, error: submitError } = useSubmitFormResponse();
  const [formResponses, setFormResponses] = useState<Record<string, any>>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showUserCodeModal, setShowUserCodeModal] = useState(false);
  const [userCode, setUserCode] = useState("");
  const [userCodeError, setUserCodeError] = useState("");

  if (!formId) {
    navigate({ to: '/' });
    return null;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading your form...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-500">
          <AlertCircle className="h-12 w-12 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error loading form</h2>
          <p className="text-muted-foreground">{error.message}</p>
        </div>
      </div>
    );
  }

  if (!form) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-muted-foreground">
          <FileText className="h-16 w-16 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Form not found</h2>
          <p>The form you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  const questions = form.form_questions.sort((a, b) => a.form_index - b.form_index);
  
  // Check if all required questions are filled out
  const isFormValid = questions.every((formQuestion) => {
    const question = formQuestion.question;
    if (!question.required) return true; // Non-required questions are always valid
    
    const value = formResponses[formQuestion.question.id];
    
    if (question.answer_type === 'file') {
      return value !== null && value !== undefined;
    } else if (question.answer_type === 'checkbox') {
      return Array.isArray(value) && value.length > 0;
    } else if (question.answer_type === 'boolean') {
      return value === true || value === false; // Both true and false are valid
    } else {
      return value !== null && value !== undefined && value !== '';
    }
  });
  
  // Calculate progress for required questions
  const requiredQuestions = questions.filter(q => q.question.required);
  const completedRequiredQuestions = requiredQuestions.filter((formQuestion) => {
    const question = formQuestion.question;
    const value = formResponses[question.id];
    
    if (question.answer_type === 'file') {
      return value !== null && value !== undefined;
    } else if (question.answer_type === 'checkbox') {
      return Array.isArray(value) && value.length > 0;
    } else if (question.answer_type === 'boolean') {
      return value === true || value === false;
    } else {
      return value !== null && value !== undefined && value !== '';
    }
  }).length;
  
  const progressPercentage = requiredQuestions.length > 0 
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
    
    const responses: Record<string, any> = {};
    questions.forEach((formQuestion) => {
      const questionId = formQuestion.question.id;
      const question = formQuestion.question;
      
      responses[questionId] = {
        question: question.question,
        answer_type: question.answer_type,
        value: formResponses[questionId] || null,
        required: question.required
      };
    });

    submitForm({
      user_code: userCode.trim(),
      formId: form.id,
      responses: responses
    }, {
      onSuccess: (data) => {
        console.log('Form submitted successfully:', data);
        setIsSubmitted(true);
        setShowUserCodeModal(false);
        setUserCode("");
        
        setTimeout(() => {
          setIsSubmitted(false);
          setFormResponses({});
        }, 5000); // Reset form after 5 seconds
      },
      onError: (error: any) => {
        console.error('Form submission failed:', error);
        if (error.response?.data?.message) {
          setUserCodeError(error.response.data.message);
        } else {
          setUserCodeError("An error occurred while submitting the form");
        }
      }
    });
  };
  
  return (
    <div className="min-h-screen bg-background">
      {/* Form Header */}
      <div className="text-center py-12 px-4">
        <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
          {form.name}
        </h1>
        <p className="text-base text-muted-foreground max-w-2xl mx-auto">
          Please fill out the form below. All required fields are marked with an asterisk (*).
        </p>
      </div>

      {/* Questions Container */}
      <div className="max-w-2xl mx-auto px-4 pb-12">
        {questions.length > 0 ? (
          <div className="space-y-6">
            {questions.map((question, index) => (
              <QuestionRenderer 
                key={question.id} 
                question={question.question} 
                index={index + 1}
                total={questions.length}
                onValueChange={(questionId, value) => {
                  setFormResponses(prev => ({
                    ...prev,
                    [questionId]: value
                  }));
                }}
              />
            ))}
            
            {/* Submit Button */}
            <div className="pt-6 text-center">
              {isSubmitted ? (
                <div className="text-center">
                  <div className="inline-flex items-center space-x-2 text-green-600 mb-4">
                    <CheckCircle className="h-5 w-5" />
                    <span className="font-medium">Form submitted successfully!</span>
                  </div>
                  <p className="text-sm text-muted-foreground">Your response has been recorded.</p>
                </div>
              ) : (
                <>
                  {/* Progress Indicator */}
                  {requiredQuestions.length > 0 && (
                    <div className="mb-4 text-center">
                      <div className="flex items-center justify-center space-x-2 mb-2">
                        <span className="text-sm text-muted-foreground">
                          Required questions completed:
                        </span>
                        <span className="text-sm font-medium">
                          {completedRequiredQuestions} / {requiredQuestions.length}
                        </span>
                      </div>
                      <div className="w-full max-w-xs mx-auto bg-muted rounded-full h-2">
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
                    disabled={!isFormValid || isSubmitting}
                  >
                    {isSubmitting ? "Submitting..." : "Submit Form"}
                  </Button>
                  
                  {!isFormValid && requiredQuestions.length > 0 && (
                    <p className="text-xs text-muted-foreground mt-2">
                      Please complete all required questions to submit
                    </p>
                  )}
                </>
              )}
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 mx-auto mb-3 text-muted-foreground" />
            <h2 className="text-xl font-semibold mb-2">This form is empty</h2>
            <p className="text-muted-foreground">No questions have been added yet.</p>
          </div>
        )}
      </div>

      {/* User Code Modal */}
      <Dialog open={showUserCodeModal} onOpenChange={setShowUserCodeModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <User className="h-5 w-5" />
              <span>Enter Your User Code</span>
            </DialogTitle>
            <DialogDescription>
              Please enter your unique user code to submit this form. This helps us prevent duplicate submissions.
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
                className="text-center text-lg font-mono tracking-widest"
                maxLength={6}
                autoFocus
              />
              {userCodeError && (
                <div className="flex items-center space-x-2 text-red-500 text-sm">
                  <AlertCircle className="h-4 w-4" />
                  <span>{userCodeError}</span>
                </div>
              )}
            </div>
          </div>
          
          <DialogFooter className="flex-col sm:flex-row space-y-2 sm:space-y-0">
            <Button
              variant="outline"
              onClick={() => {
                setShowUserCodeModal(false);
                setUserCode("");
                setUserCodeError("");
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
  onValueChange: (questionId: string, value: string | number | boolean | string[] | { name: string; size: number; type: string; lastModified: number } | null) => void;
}

function QuestionRenderer({ question, index, total, onValueChange }: QuestionRendererProps) {
  const [value, setValue] = useState<string | number | boolean | string[]>("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string>("");

  const validateInput = (input: string | number | boolean | string[]) => {
    if (question.required) {
      if (typeof input === 'boolean') {
        // For boolean fields, both true and false are valid values
        if (input === undefined || input === null) {
          setError("This field is required");
          return false;
        }
      } else if (typeof input === 'string') {
        if (!input || input.trim() === '') {
          setError("This field is required");
          return false;
        }
      } else if (typeof input === 'number') {
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
    if (question.answer_type === 'text' && typeof input === 'string' && input.trim() !== '') {
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
      case 'text': return <FileText className="h-5 w-5" />;
      case 'number': return <Hash className="h-5 w-5" />;
      case 'boolean': return <CheckSquare className="h-5 w-5" />;
      case 'radio': return <Circle className="h-5 w-5" />;
      case 'checkbox': return <Square className="h-5 w-5" />;
      case 'select': return <ChevronDown className="h-5 w-5" />;
      case 'file': return <Upload className="h-5 w-5" />;
      default: return <FileText className="h-5 w-5" />;
    }
  };

  const getFileTypeDescription = (mimeType: string) => {
    switch (mimeType) {
      case 'image/*': return 'Images (jpg, png, gif, etc.)';
      case 'application/pdf': return 'PDF files';
      case 'application/msword': return 'Word documents (.doc)';
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': return 'Word documents (.docx)';
      case 'text/csv': return 'CSV files';
      case 'text/plain': return 'Text files (.txt)';
      case 'application/vnd.ms-excel': return 'Excel files (.xls)';
      case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': return 'Excel files (.xlsx)';
      case 'application/zip': return 'ZIP archives';
      case '*/*': return 'All file types';
      default: return mimeType;
    }
  };

  const renderInput = () => {
    switch (question.answer_type) {
      case 'text': {
        return (
          <Textarea
            placeholder="Type your answer here"
            value={value as string}
            onChange={(e) => handleInputChange(e.target.value)}
            className="py-2 px-3 border-2 focus:border-primary"
            maxLength={question.max_len > 0 ? question.max_len : undefined}
          />
        );
      }

      case 'number': {
        return (
          <Input
            type="number"
            placeholder="Enter a number..."
            value={value as number}
            onChange={(e) => handleInputChange(parseInt(e.target.value) || '')}
            className="py-2 px-3 border-2 focus:border-primary"
          />
        );
      }

      case 'boolean': {
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

      case 'radio': {
        const radioOptions = question.options ? question.options.split('||') : [];
        return (
          <RadioGroup
            value={value as string}
            onValueChange={(newValue) => handleInputChange(newValue)}
            className="space-y-2"
          >
            {radioOptions.map((option) => (
              <div key={option} className="flex items-center space-x-2">
                <RadioGroupItem value={option} id={`radio-${question.id}-${option}`} />
                <Label htmlFor={`radio-${question.id}-${option}`} className="text-sm cursor-pointer">
                  {option}
                </Label>
              </div>
            ))}
          </RadioGroup>
        );
      }

      case 'checkbox': {
        const checkboxOptions = question.options ? question.options.split('||') : [];
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
                      handleInputChange(currentValues.filter(v => v !== option));
                    }
                  }}
                />
                <Label htmlFor={`checkbox-${question.id}-${option}`} className="text-sm cursor-pointer">
                  {option}
                </Label>
              </div>
            ))}
          </div>
        );
      }

      case 'select': {
        const selectOptions = question.options ? question.options.split('||') : [];
        return (
          <Select value={value as string} onValueChange={(newValue) => handleInputChange(newValue)}>
            <SelectTrigger className="w-full py-2 px-3 border-2 border-muted-foreground/10 focus:border-primary">
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

      case 'file': {
        return (
          <div className="space-y-3">
            <div className="border-2 border-dashed border-muted-foreground rounded-lg p-6 text-center hover:border-primary transition-colors cursor-pointer">
              <input
                type="file"
                accept={question.file_type !== 'none' ? question.file_type : undefined}
                onChange={(e) => {
                  const selectedFile = e.target.files?.[0];
                  if (selectedFile) {
                    setFile(selectedFile);
                    // For file uploads, validate file size in MB
                    const fileSizeMB = selectedFile.size / (1024 * 1024);
                    
                    if (question.required && !selectedFile) {
                      setError("This field is required");
                    } else if (question.min_len > 0 && fileSizeMB < question.min_len) {
                      setError(`File size must be at least ${question.min_len} MB`);
                    } else if (question.max_len > 0 && fileSizeMB > question.max_len) {
                      setError(`File size must be less than ${question.max_len} MB`);
                    } else {
                      setError("");
                      // Call onValueChange with file information
                      onValueChange(question.id, {
                        name: selectedFile.name,
                        size: selectedFile.size,
                        type: selectedFile.type,
                        lastModified: selectedFile.lastModified
                      });
                    }
                  }
                }}
                className="sr-only"
                id={`file-${question.id}`}
              />
              <label htmlFor={`file-${question.id}`} className="cursor-pointer">
                <Upload className="h-8 w-8 mx-auto mb-3 text-muted-foreground" />
                <p className="text-sm font-medium mb-1">Click to upload a file</p>
                <p className="text-xs text-muted-foreground">
                  {question.file_type !== 'none' && question.file_type !== '*/*' 
                    ? `Accepted: ${getFileTypeDescription(question.file_type)}` 
                    : 'All file types accepted'}
                </p>
                {(question.min_len > 0 || question.max_len > 0) && (
                  <p className="text-xs text-muted-foreground mt-1">
                    Size: {question.min_len > 0 ? `${question.min_len} MB` : '0 MB'} - {question.max_len > 0 ? `${question.max_len} MB` : 'Unlimited'}
                  </p>
                )}
              </label>
            </div>
            {file && (
              <div className="flex items-center space-x-2 p-2 bg-muted rounded-lg">
                <FileText className="h-4 w-4 text-primary" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setFile(null);
                    onValueChange(question.id, null);
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
          </div>
        );
      }

      default:
        return <Input placeholder="Unsupported question type" disabled />;
    }
  };

  return (
    <Card className="shadow-none rounded-md hover:shadow-xl shadow-accent/10 transition-shadow">
      <CardHeader>
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary">
            {getQuestionIcon()}
          </div>
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-0">
              <span className="text-xs text-muted-foreground font-medium bg-background/20 px-1 py-0.5 rounded-md">
                Question {index} of {total}
              </span>
              {question.required && (
                <span className="text-red-500 text-xs font-medium">*</span>
              )}
            </div>
            <CardTitle className="text-lg leading-relaxed">
              {question.question}
            </CardTitle>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        {/* Input Field */}
        {renderInput()}

        {/* Error Message */}
        {error && (
          <div className="flex items-center space-x-2 text-red-500 text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        {/* Character Count for Text Inputs */}
        {(question.answer_type === 'text' && question.max_len > 0) && (
          <div className="text-right text-xs text-muted-foreground">
            {(value as string)?.length || 0} / {question.max_len} characters
          </div>
        )}
      </CardContent>
    </Card>
  );
}
