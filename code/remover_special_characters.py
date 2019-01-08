#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Alfonso Barragán Carmona
# Marcos López Sobrino
# Roberto Plaza Romero

def remove_special_characters(input_path, output_path):
    file_in     = open(input_path, 'r')
    file_out    = open(output_path, 'w')
    output = ""

    line = file_in.readline()
    while line:
        new_line = line.decode('utf8')
        line_to_write = new_line.encode('cp1250')

        print line_to_write
        output += line_to_write

        line = file_in.readline()
    
    file_in.close()
    file_out.close()
    
if __name__ == '__main__':
    remove_special_characters('../data_to_test/data_flume/FlumeData.1516810243169', '../data_to_test/lel.txt')