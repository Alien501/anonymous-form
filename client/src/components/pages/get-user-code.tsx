import { UserIcon } from "lucide-react";
import { Button } from "../ui/button";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTrigger } from "../ui/dialog";
import { Input } from "../ui/input";
import { useState, useEffect } from "react";
import { useUserCode } from "~/lib/api/form/useUserCode";

export default function GetUserCode(){
    const [email, setEmail] = useState('');
    const [error, setError] = useState<string | null>(null);
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const { mutate: sendUserCode, isPending, error: mutationError, isSuccess } = useUserCode();
    
    // Reset email state when mail is sent successfully
    useEffect(() => {
        if (isSuccess) {
            setEmail('');
            setError(null);
        }
    }, [isSuccess]);
    
    const handleInputChange = (value: string) => {
        setEmail(prev => value);
        // Clear error when user starts typing
        if (error) setError(null);
    }
    
    const onSendMailClick = async () => {
        if(email.trim().length == 0 || !emailRegex.test(email)) {
            setError("Enter valid mail address to continue");
            return;
        }
        
        setError(null);
        sendUserCode(email);
    }

    return(
        <Dialog>
            <DialogTrigger asChild>
                <Button><span><UserIcon /></span> User Code</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <div className="flex text-lg items-center font-medium space-x-2"><span><UserIcon size={24} /></span><h1>Get User Code</h1></div>
                </DialogHeader>
                <div className="flex flex-col space-y-3">
                    <p>Enter your email, user code will be sent to that, don't share it with anyone</p>
                    <Input value={email} onChange={(e) => handleInputChange(e.target.value)} type="email" placeholder="Email" />
                    {
                        error && (
                            <p className="text-destructive text-sm font-medium">{error}</p>
                        )
                    }
                    {
                        mutationError && (
                            <p className="text-destructive text-sm font-medium">
                                {mutationError.message || "Failed to send user code. Please try again."}
                            </p>
                        )
                    }
                    {
                        isSuccess && (
                            <p className="text-green-600 text-sm font-medium">User code sent successfully to your email!</p>
                        )
                    }
                    <Button 
                        disabled={email.trim().length == 0 || !emailRegex.test(email) || isPending} 
                        onClick={onSendMailClick}
                    >
                        {isPending ? "Sending..." : "Send User Code"}
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    )
}