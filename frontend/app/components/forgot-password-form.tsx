import { cn } from "~/lib/utils";
import { Button } from "~/components/ui/button";
import { Card, CardContent } from "~/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { useContext } from "react";
import { AuthContext, type UserType } from "~/contexts/AuthContext";
import api from "~/lib/api";
import { toast } from "sonner";

export function ForgotPasswordForm({
  className,
  user,
  ...props
}: { user: UserType } & React.ComponentProps<"div">) {
  const { login } = useContext(AuthContext);

  const sendResetLink = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const email = data.get("email") as string;

    if (!email) {
      return;
    }

    const userApi = user === "seller" ? api.sellers : api.partners;
    await userApi.forgotPassword({ email });
    toast("Reset link has been sent to your email.");
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={sendResetLink}>
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center">
                <h1 className="text-2xl font-bold">Reset Password</h1>
                <p className="text-balance text-muted-foreground">
                  Enter your email address
                </p>
              </div>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="m@example.com"
                  required
                />
              </Field>
              <Field>
                <Button type="submit">Login</Button>
              </Field>
            </FieldGroup>
          </form>
          <div className="relative hidden bg-muted md:block">
            <img
              src="/rider.jpg"
              alt="Image"
              className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
