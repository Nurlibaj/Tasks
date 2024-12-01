"""
Exercise 1:
Create a Pizza class that could have ingredients added to it. Raise an error if an attempt is made to add a duplicate ingredient.
"""
import math
import random

from numpy.matrixlib.defmatrix import matrix


class Pizza:
    def __init__(self):
        self.ingredients=set()
    
    def add_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            raise ValueError(f'{ingredient} already added')
        else:
            self.ingredients.add(ingredient)


"""
Exercise 2:
Create an Elevator class with methods to go up, go down, and get the current floor. The elevator should not be able to go below the ground floor (floor 0).
"""
class Elevator:
    def __init__(self):
        self.current_floor=0

    def go_up(self):
        self.current_floor+=1

    def go_down(self):
        if self.current_floor==0:
            pass
        else:
            self.current_floor-=1

    def get_current_floor(self):
        return self.current_floor


"""
Exercise 3:
Create a class Stack with methods to push, pop, and check if the stack is empty. Raise an exception if a pop is attempted on an empty stack.
"""
class Stack:
    def __init__(self):
        self.arr=[]

    def push(self, item):
        self.arr.append(item)

    def pop(self):
        if len(self.arr)==0:
            raise  IndexError("Stack is empty")
        else:
            return self.arr.pop()

    def is_empty(self):
        if len(self.arr)==0:
            return True
        else:
            return False


"""
Exercise 4:
Design a BankAccount class with methods to deposit, withdraw, and check balance. Ensure that an account cannot go into a negative balance.
"""
class BankAccount:
    def __init__(self, initial_balance):
        self.balance=initial_balance

    def deposit(self, amount):
        self.balance+=amount

    def withdraw(self, amount):
        if self.balance-amount<0:
            raise ValueError(f'{self.balance} is empty')
        else:
            self.balance-=amount

    def check_balance(self):
        return self.balance


"""
Exercise 5:
Create a class Person with attributes for name and age. Implement a method birthday that increases the person's age by one. Raise an exception if an age less than 0 is entered.
"""
class Person:
    def __init__(self, name, age):
        self.name=name
        if age < 0:
            raise ValueError(f'{age} less than zero')
        else:
            self.age = age


    def birthday(self):
        self.age+=1




"""
Exercise 6:
Create an Animal base class and a Dog and Cat derived classes. Each animal should have a sound method which returns the sound they make.
"""
class Animal:
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cat(Animal):
    def sound(self):
        return  "Meow"


"""
Exercise 7:
Design a class Calculator with static methods for addition, subtraction, multiplication, and division. Division method should raise a ZeroDivisionError when trying to divide by zero.
"""
class Calculator:
    @staticmethod
    def add(x, y):
        return x+y

    @staticmethod
    def subtract(x, y):
        return x-y

    @staticmethod
    def multiply(x, y):
        return x*y

    @staticmethod
    def divide(x, y):
        if y==0:
            raise  ZeroDivisionError("Cannot divide to zero")
        return x/y


"""
Exercise 8:
Create a class `Car` with attributes for speed and mileage. Raise a ValueError if a negative value for speed or mileage is entered.
"""
class Car:
    def __init__(self, speed, mileage):
        if speed<0:
            raise ValueError("Cannot set negative value")
        if mileage<0:
            raise ValueError("Mileage can't be negative")
        self.speed=speed
        self.mileage=mileage



"""
Exercise 9:
Create a Student class and a Course class. Each Course can enroll students and print a list of enrolled students.
"""
class Student:
    def __init__(self, name):
        self.name=name

class Course:
    def __init__(self):
        self.students=[]

    def enroll(self, student):
        self.students.append(student)

    def print_students(self):
        return self.students


"""
Exercise 10:
Create a Flight class with a destination, departure time, and a list of passengers. Implement methods to add passengers, change the destination, and delay the flight by a certain amount of time.
"""
class Flight:
    def __init__(self, destination, departure):
        self.destination=destination
        self.departure=departure
        self.passengers=[]

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def change_destination(self, new_destination):
        self.destination=new_destination

    def delay(self, delay_time):
        hour=int(self.departure[:2])+delay_time
        if hour==24:
            hour="00"
        elif hour<10:
            hour="0"+str(hour)
        else:
            hour=str(hour)
        self.departure=hour+self.departure[2:]

"""
Exercise 11:
Create a Library class with a list of Book objects. The Book class should have attributes for title and author. The Library class should have methods to add books and find a book by title.
"""
class Book:
    def __init__(self, title, author):
        self.title=title
        self.author=author

class Library:
    def __init__(self):
        self.books=[]

    def add_book(self, book):
        self.books.append(book)

    def find_by_title(self, title):
        for i in self.books:
            if i.title==title:
                return i
        return "Not found"


"""
Exercise 12:
Design a class Matrix that represents a 2D matrix with methods for addition, subtraction, and multiplication. Implement error handling for operations that are not allowed (e.g., adding matrices of different sizes).
"""
class Matrix:
    def __init__(self, matrix):
        self.matrix=matrix

    def add(self, other):
        if self.check(other):
            result = [
                [
                    self.matrix[i][j] + other.matrix[i][j]
                    for j in range(len(self.matrix[0]))
                ]
                for i in range(len(self.matrix))
            ]
            return Matrix(result)
        else:
            raise ValueError("size of two matrix is different")

    def subtract(self, other):
        if self.check(other):
            result = [
                [
                    self.matrix[i][j] - other.matrix[i][j]
                    for j in range(len(self.matrix[0]))
                ]
                for i in range(len(self.matrix))
            ]
            return Matrix(result)
        else:
            raise ValueError("size of two matrix is different")

    def multiply(self, other):
        if self.check(other):
            result = [
                [
                    sum(self.matrix[i][k] * other.matrix[k][j] for k in range(len(other.matrix)))
                    for j in range(len(other.matrix[0]))
                ]
                for i in range(len(self.matrix))
            ]
            return Matrix(result)
        else:
            raise ValueError("size of two matrix is different")
    def check(self,other):
        if len(self.matrix) != len(other.matrix):
            return False
        for i in range(len(self.matrix)):
            if len(self.matrix[i]) != len(other.matrix[i]):
                return False
        return True



"""
Exercise 13:
Create a class Rectangle with attributes for height and width. Implement methods for calculating the area and perimeter of the rectangle. Also, implement a method is_square that returns true if the rectangle is a square and false otherwise.
"""
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height


"""
Exercise 14:
Design a class Circle with attributes for radius. Implement methods for calculating the area and the circumference of the circle. Handle exceptions for negative radius values.
"""
class Circle_ex14:
    def __init__(self, radius):
        if radius<0:
            raise ValueError("Can't be negative value")
        self.radius=radius

    def area(self):
        return math.pi*self.radius*self.radius

    def circumference(self):
        return 2*math.pi*self.radius


"""
Exercise 15:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class Triangle_ex15:
    def __init__(self, side_a, side_b, side_c):
       if (side_a+side_b)>side_c and (side_a+side_c)>side_b and (side_b+side_c)>side_a:
            self.side_a=side_a
            self.side_b=side_b
            self.side_c=side_c
       else:
           raise ValueError("Can't exists triangle with given sides")


    def area(self):
            half_per = self.perimeter() / 2
            res = math.sqrt(half_per * (half_per - self.side_a) * (half_per - self.side_b) * (half_per - self.side_c))
            return res

    def perimeter(self):
            return self.side_a+self.side_b+self.side_c


"""
Exercise 16:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class AbstractShape:
    def area1(self):
        pass

    def perimeter1(self):
        pass

class Circle(AbstractShape):
    def __init__(self, radius):
        pass

class Rectangle1(AbstractShape):
    def __init__(self, height, width):
        pass

class Triangle(AbstractShape):
    def __init__(self, side_a, side_b, side_c):

        self.side_a=side_a
        self.side_b=side_b
        self.side_c=side_c
    def is_triangle(self):
        if (self.side_a+self.side_b>self.side_c) and (self.side_a+self.side_c>self.side_b) and (self.side_b+self.side_c>self.side_a):
            return True
        else:
            raise ValueError("Can't exists triangle with given sides")
    def perimeter1(self):
        if self.is_triangle():
            return self.side_a+self.side_b+self.side_c
    def area1(self):
        if self.is_triangle():
            half_per=self.perimeter1()/2
            res=math.sqrt(half_per*(half_per-self.side_a)*(half_per-self.side_b)*(half_per-self.side_c))
            return  res
"""
Exercise 17:
Create a MusicPlayer class that contains a list of songs and methods to add songs, play a song, and skip to the next song. Also implement a method to shuffle the playlist.
"""
class MusicPlayer:
    def __init__(self):
        self.playlist=[]
        self.current_song=None
        self.idx=None

    def add_song(self, song):
        self.playlist.append(song)

    def play_song(self):
        if self.playlist:
            if self.idx==None:
                self.idx=0
            self.current_song=self.playlist[self.idx]
        else:
            raise ValueError("No songs in playlist")

    def next_song(self):
        if self.playlist:
            self.idx+=1
            self.current_song=self.playlist[self.idx]
        if self.idx>=len(self.playlist):
            self.idx=0
            self.current_song=self.playlist[self.idx]

    def shuffle(self):
        random.shuffle(self.playlist)


"""
Exercise 18:
Design a Product class for an online store with attributes for name, price, and quantity. Implement methods to add stock, sell product, and check stock levels. Include error handling for attempting to sell more items than are in stock.
"""
class Product:
    def __init__(self, name, price, quantity):
        self.name=name
        self.price=price
        self.quantity=quantity

    def add_stock(self, quantity):
        self.quantity+=quantity

    def sell(self, quantity):
        if self.quantity-quantity<0:
            raise ValueError(f'Store has not {quantity} items')
        else:
            self.quantity-=quantity

    def check_stock(self):
        return self.quantity


"""
Exercise 19:
Create a VideoGame class with attributes for title, genre, and rating. Implement methods to change the rating, change the genre, and display game details.
"""
class VideoGame:
    def __init__(self, title, genre, rating):
        self.title=title
        self.genre=genre
        self.rating=rating

    def change_rating(self, rating):
        self.rating=rating

    def change_genre(self, genre):
        self.genre=genre

    def display_details(self):
        return f'{self.title} video game with genre {self.genre} and rating {self.rating} '


"""
Exercise 20:
Create a School class with a list of Teacher and Student objects. Teacher and Student classes should have attributes for name and age. The School class should have methods to add teachers, add students, and print a list of all people in the school.
"""
class Human:
    def __init__(self, name, age):
        pass


class Teacher(Human):
    def __init__(self,name,age):
        self.name=name
        self.age=age

class Students(Human):
    def __init__(self,name,age):
        self.name=name
        self.age=age


class School:
    def __init__(self):
        self.students=[]
        self.teachers=[]

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_student(self, student):
        self.students.append(student)

    def get_all(self):
        return self.teachers + self.students

"""
Exercise 21:
Design a Card class to represent a playing card with suit and rank. Then design a Deck class that uses the Card class. The Deck class should have methods to shuffle the deck, deal a card, and check the number of remaining cards.
"""
class Card:
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank

class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def count(self):
        return len(self.cards)
