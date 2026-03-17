import React, { type InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ label, className = '', id, ...props }, ref) => {
        return (
            <div className="flex flex-col space-y-2 w-full">
                {label && (
                    <label htmlFor={id} className="text-sm font-semibold text-[#212529] ml-1">
                        {label}
                    </label>
                )}
                <input
                    ref={ref}
                    id={id}
                    className={`px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#007BFF]/20 focus:border-[#007BFF] transition-all duration-200 placeholder:text-gray-400 ${className}`}
                    {...props}
                />
            </div>
        );
    }
);
Input.displayName = 'Input';
