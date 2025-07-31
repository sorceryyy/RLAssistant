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
        CustomArgs("--batch-size", target="training_params.batch_size", kargs={
            'type': int,
            'help': 'Batch size for training'
        })
    ]
    
    # Specify the config file name
    config_file = "example_params.json"
    
    # Parse arguments
    configs = rla_get_args(config_file, options)
    
    # Print the parsed configurations
    print("Parsed configurations:", configs)

if __name__ == "__main__":
    main()
