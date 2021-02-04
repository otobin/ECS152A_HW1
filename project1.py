import sys


# Read in a file and return an array of strings where each string is the content of the line.
def read_file(input_file):
    f = open(input_file)
    data = [item.strip() for item in f.readlines()]
    f.close()
    return data


# Takes in a list of strings where each string is a line in the database file and creates a list of range objects using
# the data from the database file
def read_db(data_array):
    range_list = []
    for i in range(0, len(data_array)):
        line = data_array[i].split(" ")
        # Check that the line isn't empty
        if line[0]:
            range_object = Range(line[0], line[1], line[2])
            range_list.append(range_object)
    return range_list


# Converts a number to a list of 0's and 1's that represent the number in binary. Padded with 0's so it is guaranteed
# to be of length 8.
def convert_to_binary(num):
    binary_array = []
    while num > 0:
        remainder = num % 2
        num = num // 2
        binary_array.insert(0, remainder)
    # Pad with 0's to return an array of 8
    current_binary_array_length = len(binary_array)
    for i in range(0, 8 - current_binary_array_length):
        binary_array.insert(0, 0)
    return binary_array


# Takes in an array of 0's and 1's of length 8 that represents the number in binary and returns the decimal.
def convert_from_binary(binary_array):
    num_in_decimal = 0
    current_power = 7
    for i in range(0, len(binary_array)):
        if binary_array[i] == 1:
            num_in_decimal += pow(2, current_power)
        current_power -= 1
    return num_in_decimal


# Takes in a list of record objects and returns the record object with the longest prefix
def find_max_overlap(record_list):
    max_record = record_list[0]
    for i in range(1, len(record_list)):
        if record_list[i].prefix > max_record.prefix:
            max_record = record_list[i]
    return max_record


# Range class represents the range of IP addresses held by an IP address and prefix.
class Range:

    # Constructor takes in IP address as string eg: "3.218.160.0", prefix length as a string,
    # and the AS number as a string. The object then uses the prefix and starting IP to find the ending IP
    def __init__(self, string_ip, prefix, as_number):
        self.string_start_range = string_ip
        self.prefix = int(prefix)
        self.as_number = int(as_number)
        self.string_end_range = self.get_string_end_range()

    # Returns a string in the form "a.b.c.d" that represents the final IP address in the range
    def get_string_end_range(self):
        start_range = self.string_start_range
        prefix = self.prefix
        start_range_array = start_range.split(".")
        index_of_changed = prefix // 8
        # If prefix is 32, then the start range is the same as the end range
        if index_of_changed == 4:
            return self.string_start_range
        remainder = prefix % 8
        if (start_range_array[index_of_changed] == ''):
            start_range_array[index_of_changed] = 0
        # Change the number in the middle of the prefix
        num_to_modify = int(start_range_array[index_of_changed])
        # Convert to binary
        binary_array = convert_to_binary(num_to_modify)
        # Set the rest of the bits to 1
        for i in range(remainder, 8):
            binary_array[i] = 1
        # Convert back to decimal
        new_num = convert_from_binary(binary_array)
        start_range_array[index_of_changed] = new_num
        # Fill in the remaining elements with 255
        for i in range(index_of_changed + 1, len(start_range_array)):
            start_range_array[i] = 255
        # Change back to a string format
        return_string = ""
        for i in range(0, len(start_range_array)):
            return_string += str(start_range_array[i])
            if i != len(start_range_array) - 1:
                return_string += "."
        return return_string

    # Takes in a string in the form "a.b.c.d" representing an IP Address and returns whether the range overlaps
    # with it
    def is_overlapping(self, ip_string):
        ip_array = ip_string.split(".")
        range_start_array = self.string_start_range.split(".")
        range_end_array = self.string_end_range.split(".")
        for i in range(0, len(ip_array)):
            start = int(range_start_array[i])
            end = int(range_end_array[i])
            current_num = int(ip_array[i])
            if not (start <= current_num <= end):
                return False
        return True


if __name__ == "__main__":
    db_input = read_file(sys.argv[1])
    db_list = read_db(db_input)
    ip_input = read_file(sys.argv[2])
    # Map each Ip_input to a list of Range objects that they overlap with
    overlapping_hash = {}
    for i in range(0, len(ip_input)):
        current_ip = ip_input[i]
        overlapping_hash[current_ip] = []
        for j in range(0, len(db_list)):
            db = db_list[j]
            if db.is_overlapping(current_ip):
                overlapping_hash[current_ip].append(db)
    # For each IP, get the record with the longest prefix and print out in the correct format
    for ip in overlapping_hash.keys():
        destination_ip = find_max_overlap(overlapping_hash[ip])
        # Eg: 208.0.0.0/11  1239 208.30.172.70
        return_string = destination_ip.string_start_range + '/' + str(destination_ip.prefix) + " " + \
                        str(destination_ip.as_number) + " " + ip + "\n"
        output_string = file2.readline()
