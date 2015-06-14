# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

''' This is a stack base module '''
class Stack:
                                                                      
    def __init__(self, size = 5000):
        self.stack = []     # first statement a stack
        self.size = size    # create stack size
        self.top = -1       # stack top index
        
    ''' set the stack size '''    
    def setSize(self, size):                                                
        self.size = size
        
    ''' set push action -> each for single element '''
    def push(self, element):
        ''' if stack is full, raise error of overflow '''                                                
        if self.isFull():
            raise 'The Stack is Overflow.'
        else:
            self.stack.append(element)
            self.top = self.top + 1
        
    ''' set pop action '''        
    def pop(self):
        ''' if stack is empty, raise error of empty '''
        if self.isEmpty():
            raise 'PyStackUnderflow'
        else:
            element = self.stack[-1]
            self.top = self.top - 1
            del self.stack[-1]
            return element
     
    ''' get Stack top position '''    
    def Top(self):
        
        return self.top
    
    ''' get clean of our stack '''
    def empty(self):
        self.stack = []  # cleanup our stack
        self.top = -1    # the top is clean for -1
    
    ''' judge is empty stack FROM -> stack position '''
    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False
    
    ''' judge is full stack FROM -> stack position '''    
    def isFull(self):
        if self.top == self.size - 1:
            return True
        else:
            return False