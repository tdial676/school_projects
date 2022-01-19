package edu.caltech.cs2.project02.choosers;

import edu.caltech.cs2.project02.interfaces.IHangmanChooser;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class RandomHangmanChooser implements IHangmanChooser {
    private static String dictionary = "data/scrabble.txt";
    private static final Random rand = new Random();
    private final String secretWord;
    private  int remainingGuesses;
    private SortedSet<Character> guesses;

  public RandomHangmanChooser(int wordLength, int maxGuesses) throws FileNotFoundException {
    if (wordLength < 1 || maxGuesses < 1) {
      throw new IllegalArgumentException("Both Word length and max guesses must be greater than or equal to 1.");
    }
    Scanner scanner = new Scanner(new File(dictionary));
    SortedSet<String> choices = new TreeSet<>();
    String hold2 = null;
    while (scanner.hasNextLine()) {
      hold2 = scanner.nextLine();
      if (hold2.length() == wordLength) {
        choices.add(hold2);
      }
    }
    scanner.close();
    if (choices.size() == 0) {
      throw new IllegalStateException(" A word of the provided length, "+ wordLength + ", is out of range");
    }
    int index = rand.nextInt(choices.size());
    int i = 0;
    String holder = "";
    for ( String word : choices) {
      if (i == index) {
        holder = word;
      }
      i++;
    }
    this.secretWord = holder;
    this.remainingGuesses = maxGuesses;
    this.guesses = new TreeSet<>();

  }    

  @Override
  public int makeGuess(char letter) {
    if (letter < 'a' || letter > 'z') {
      throw new IllegalArgumentException("The guessed letter must be in lowercase form.");
    }
    if (this.remainingGuesses < 1) {
      throw new IllegalStateException( "You have no more guesses left");
    }
    if (guesses.contains(letter)){
      throw new IllegalArgumentException("You have already guessed the letter: " + letter);
    }
    this.guesses.add(letter);
    int count = 0;
    for (int i = 0; i < this.secretWord.length(); i++) {
      if (this.secretWord.charAt(i) == letter) {
        count++;
      }
    }
    if (count == 0) {
      this.remainingGuesses--;
    }
    return count;
  }

  @Override
  public boolean isGameOver() {
    int holder = 0;
    String order = getPattern();
    for (int i = 0; i < order.length(); i++) {
      if (order.charAt(i) == '-') {
        holder++;
      }
    }
    return (this.remainingGuesses < 1 || holder == 0);
  }

  @Override
  public String getPattern() {
    String holder = "";
    for (int i = 0; i < this.secretWord.length(); i++) {
      if (this.guesses.contains(this.secretWord.charAt(i))) {
        holder += this.secretWord.charAt(i);
      } else {
        holder += '-';
      }
    }
    return holder;
  }

  @Override
  public SortedSet<Character> getGuesses() {
    return this.guesses;
  }

  @Override
  public int getGuessesRemaining() {
    return this.remainingGuesses;
  }

  @Override
  public String getWord() {
    this.remainingGuesses = 0;
    return this.secretWord;
  }
}