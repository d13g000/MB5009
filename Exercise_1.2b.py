import sys  # Import sys to handle command-line arguments


def phred33_to_quality(quality_string):
    """Convert Phred+33 encoded quality string to a list of quality scores."""
    return [ord(char) - 33 for char in quality_string]  # Convert ASCII
    # character to quality score


def filter_fastq(file_path, mean_quality):
    """Filter out sequences with mean quality below the user-defined
    threshold."""
    with open(file_path, 'r') as file:  # Open the input FASTQ file
        lines = file.readlines()  # Read all lines from the file

    output_lines = []  # List to store filtered FASTQ entries
    total_sequences = len(lines) // 4  # Calculate total sequences in input file
    filtered_out_count = 0  # Counter for number of sequences removed

    for i in range(0, len(lines), 4):  # Loop through the file in FASTQ format
        header = lines[i].strip()  # First line: Sequence identifier
        sequence = lines[i + 1].strip()  # Second line: DNA sequence
        plus = lines[i + 2].strip()  # Third line: Separator (+)
        quality = lines[i + 3].strip()  # Fourth line: Quality scores

        quality_scores = phred33_to_quality(quality)  # Convert quality
        # string to scores
        sequence_mean_quality = sum(quality_scores) / len(quality_scores)
        # Calculate mean quality score of the sequence

        if sequence_mean_quality >= mean_quality:  # If sequence quality is
            # above or equal to threshold
            output_lines.extend([header, sequence, plus, quality])  # Add
            # sequence to output list
        else:
            filtered_out_count += 1  # Increment the count of filtered out
            # sequences

    remaining_sequences = total_sequences - filtered_out_count  # Calculate
    # remaining sequences

    if not output_lines:  # If no sequences remain after filtering
        print("Warning: No sequences remain after filtering.")  # Notify the
        # user

    output_file = file_path.replace(".fastq", "_filtered.fastq")  # Create
    # output file name
    with open(output_file, 'w') as file:  # Open the output file for writing
        file.write("\n".join(output_lines) + "\n")  # Write the modified
        # FASTQ data

    print(f"Filtering complete. Output saved to {output_file}")  # Notify
    # user of success
    print(f"Total sequences in input file: {total_sequences}")  # Print total
    # sequences before filtering
    print(f"Sequences removed: {filtered_out_count}")  # Print number of
    # sequences filtered out
    print(f"Sequences remaining in output file: {remaining_sequences}")
    # Print number of sequences in filtered file


if __name__ == "__main__":  # Ensure script runs only when executed directly
    if len(sys.argv) != 3:  # Check if the correct number of arguments are
        # provided
        print("Usage: python script.py <input_file> <mean_quality>")  # Print
        #  usage instructions
        sys.exit(1)  # Exit script with an error

    input_file = sys.argv[1]  # Get the input FASTQ file name from
    # command-line argument
    mean_quality = float(sys.argv[2])  # Get the user-defined mean quality
    # threshold
    filter_fastq(input_file, mean_quality)  # Call function to process the
    # FASTQ file