import React, { ButtonHTMLAttributes } from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'outline';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = '', variant = 'primary', fullWidth, children, ...props }, ref) => {
    let baseStyles = 'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-xl text-sm px-5 py-3';
    
    let variantStyles = '';
    switch (variant) {
      case 'primary':
        variantStyles = 'bg-[#007BFF] hover:bg-blue-700 text-white focus:ring-[#007BFF]';
        break;
      case 'secondary':
        variantStyles = 'bg-[#FF8255] hover:bg-orange-600 text-white focus:ring-[#FF8255]';
        break;
      case 'ghost':
        variantStyles = 'bg-transparent hover:bg-gray-100 text-[#212529] focus:ring-gray-200';
        break;
      case 'outline':
        variantStyles = 'bg-transparent border border-gray-300 hover:bg-gray-50 text-[#212529] focus:ring-gray-200';
        break;
    }

    const widthStyles = fullWidth ? 'w-full' : '';
    const disabledStyles = props.disabled ? 'opacity-50 cursor-not-allowed pointer-events-none' : '';

    return (
      <button
        ref={ref}
        className={`${baseStyles} ${variantStyles} ${widthStyles} ${disabledStyles} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';
