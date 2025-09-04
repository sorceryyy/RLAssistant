from RLA.rla_argparser import CustomArgs, CustomBoolArgs, rla_get_args

def main():
    """
    Example of using RLA's argument parser with different data types
    """
    options = [
        # Basic data types examples
        CustomArgs("--name", target="basic_params.name", kargs={'type': str, 'help': 'Example of string type'}),
        CustomArgs("--age", target="basic_params.age", kargs={'type': int, 'help': 'Example of integer type'}),
        CustomArgs("--score", target="basic_params.score", kargs={'type': float, 'help': 'Example of float type'}),
        
        # Boolean type examples
        CustomBoolArgs("--is-student", target="bool_params.is_student", kargs={'help': 'Example of boolean type'}),
        CustomBoolArgs("--has-experience", target="bool_params.has_experience", kargs={'help': 'Another boolean example'}),
        
        # List type examples
        CustomArgs("--grades", target="list_params.grades", kargs={
            'type': float,
            'nargs': '+',  # '+' means one or more arguments
            'help': 'Example of float list type'
        }),
        CustomArgs("--subjects", target="list_params.subjects", kargs={
            'type': str,
            'nargs': '*',  # '*' means zero or more arguments
            'help': 'Example of string list type'
        }),
        
        # Advanced examples
        CustomArgs("--learning-rate", target="training_params.lr", kargs={
            'type': float,
            'help': 'Learning rate for training'
        }),
    ]
    
    # Specify the config file name
    config_file = "example_params.json"
    
    # Parse arguments
    configs = rla_get_args(config_file, options)
    
    # Print the parsed configurations
    print("Parsed configurations:", configs)

if __name__ == "__main__":
    """
    Usage Examples:
    
    In addition to the predefined custom arguments (which serve as convenient shortcuts),
    RLA automatically appends any additional command-line arguments to the configuration
    using the standard --key=value format.
    
    For boolean arguments, RLA supports two formats:
    - Use --key to set the value to True
    - Use --no-key to set the value to False
    
    Example command-line usage:
    
    1. Basic usage with predefined arguments:
       python script.py --name "Alice" --age 25 --score 95.5 --is-student --training_params.batch_size 128
    
    2. Using list arguments:
       python script.py --grades 85.5 90.0 88.5 --subjects "Math" "Science" "English"
    
    3. Using boolean arguments (both formats):
       python script.py --is-student --no-has-experience
    
    4. Combining predefined and additional arguments:
       python script.py --name "Bob" --custom-param=value --another-flag=true
    
    5. Complete example:
       python script.py --name "Charlie" --age 30 --score 92.0 --is-student \
                       --grades 88.0 91.5 89.0 --subjects "Physics" "Chemistry" \
                       --learning-rate 0.01 --batch-size 64 \
                       --custom-optimizer="Adam" --use-gpu=true
    """

    main()
