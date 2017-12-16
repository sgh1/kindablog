---
title: Macroless C++ Unit Tests
date: 2017.6.10
tags: c++, testing
---

WHY\_DO\_ALL\_CPP\_UNIT\_TESTING\_FRAMEWORKS\_USE\_TONS\_OF\_MACROS? I am slightly put off by:

```cpp
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Suites
#include <boost/test/unit_test.hpp>


int add(int i, int j)
{
    return i + j;
}

BOOST_AUTO_TEST_SUITE(Maths)

BOOST_AUTO_TEST_CASE(universeInOrder)
{
    BOOST_CHECK(add(2, 2) == 4);
}

BOOST_AUTO_TEST_SUITE_END()

BOOST_AUTO_TEST_SUITE(Physics)

BOOST_AUTO_TEST_CASE(specialTheory)
{
    int e = 32;
    int m = 2;
    int c = 4;

    BOOST_CHECK(e == m * c * c);
}

BOOST_AUTO_TEST_SUITE_END()</boost> </pre>
```

(This is from [http://www.alittlemadness.com/2009/03/31/c-unit-testing-with-boosttest/](http://www.alittlemadness.com/2009/03/31/c-unit-testing-with-boosttest/)). I know it's a bit out of date. As much as macros seem to be universally regarded with caution by C++ programmers, we put up with them when it comes to unit testing, perhaps in part due to the following:

*   We are willing to do whatever it takes to reduce the boilerplate when writing tests. If the overhead required to write a test is high, tests are less likely to be written, and that's a Bad Thing.
*   Modern C++ (like C++17) might give us the ability to write low-boilerplate test framework, but there is still an awful lot of 98 and 03 code that needs testing, and we don't want to exclude them.
*   We want our testing framework to look more like some other testing framework from the past from a different language.

And one I've found personally after this experiment:

*   It's nice to know where the framework ends and tests begin. Sometimes, the macros used in a lot of C++ testing frameworks stand out as the framework (especially since macros, by convention, are all-caps), and you know the not-macros is the test case itself. It's the nature of the beast that we have to test in the same language as the unit, and maybe in some alternate universe, we could avoid that.

### Disclaimers

First, I know there are testing frameworks out there that aren't so macro-based, but it still seems to be a pervasive thing amongst the most popular ones. Second, this blog post is a bit of a nit-pick. I've used a few of the frameworks I'm referring to (like Google Test), and they do a good job on the whole. In other words, the macro thing isn't a deal breaker for what are otherwise pretty good solutions to the testing problem. And in general, I rely on macros, one way or another, written by me or not, everyday, so I can't fairly launch an all-out assault on them. I just thought there was enough room to see what might happen in a minimalist, macro-free testing framework.

### Concepts (no, not those concepts) For macroless

If you just want to read the code and draw your own conclusions, here's the github link: [macroless on github.](https://github.com/sgh1/macroless) The testing framework I came up with revolves around a main test class:

```cpp
class test
    {
    public:

        test(   std::string name,
                std::function<bool(test*)> r,
                std::function<void(test*)> su = [](test*){},
                std::function<void(test*)> td = [](test*){} );

        virtual ~test();

        virtual void setup(){
			this->setup_(this);
		}

        virtual bool run(){
			this->run_(this);
        }

        virtual void teardown(){
			this->teardown_(this);
		}

        std::string test_name_;

        std::function<bool(test*)> run_;
        std::function<void(test*)> setup_, teardown_;
    };
```
We have some semblance of a "normal" test class, with the teardown, setup, and run functions, and we also have some std::functions. There is some redundancy there, obviously. The reason for that is: the normal virtual functions give us a way to create a test fixture, and the std::functions, via the constructor, are what allow us to write a test in a way similar to Google's ADD_TEST, or BOOST_AUTO_TEST_CASE. The requirement of having the std::functions accept a pointer back to this is also a requirement of fixtures, which didn't really turn out too well. More on that in a moment. Let's take a look at how we would use the class. This is just a .cpp file which contains a bunch of test cases. By convention, one test-file is supposed to compiled as one binary.

```cpp
#include "macroless.h"
#include <vector>

// Do some tests on std::vector.

// Create test case vector for this test.
macroless::test_vector tests;

// Create collection function.
void std_vector_tests()
{

    // Create test cases and add them to the test vector.
    // Test size of a vector.
    tests.push_back(
            macroless::test_ptr(
                    new macroless::test(
                            "size_check",
                            [](macroless::test*)
                            {
                                // Create std vector.
                                std::vector<int> int_vector;

                                // Add some items.
                                int_vector.push_back(1);
                                int_vector.push_back(-15);
                                int_vector.push_back(21);

                                // Do the test.
                                if(int_vector.size() != 3){
                                    macroless::fail_test("The size of int_vector is",int_vector.size(),
                                                         "but it should have been 3.");
                                }

                                // If we get here, we pass the test.
                                return true;
                            }
            )));

}

// Entry point for test.
int main(int argc, char** argv) {
    return macroless::run(argc,argv,std_vector_tests,tests);
}
```

So we create a std::vector for our tests to go in, create a function (which can be of any name, in this case it's std_vector_tests) where you write and add the tests, and then just call macroless::run. Okay, this:

```cpp

tests.push_back(
            macroless::test_ptr(
                    new macroless::test(
                            "size_check",
                            [](macroless::test*)
                            {
```

Is a lot more boilerplate than this:

```cpp
ADD_TEST(size_check,...)
```

But I think there's something to be said for reading normal C++. I think, if you're a C++ programmer, you feel a bit more at home. You also have a better idea of what's going on, and how you can us the "framework". On the contrary, sometimes testing frameworks feel like they each have their own language. By the way, here is a stripped-down version of macroless::run:

```cpp

    // Function to run a std::vector of tests.
    bool run(int argc, char** argv, std::function<void()> collector,
             const test_vector& tests)
    {        

        // Run the collector.
        collector();

        // Run the tests.
        for(auto& t : tests)
        {
            // This try/catch will only catch test failures.
            try
            {
                t->setup();

                // Run the test.
                if(t->run()){
                    tests_passed++;
                    get_output() << "\tTest case " << std::setw(30) << std::left <<  t->test_name_ << " [PASSED].\n";
                }

                t->teardown();
            }

            // Catch test failure.
            catch(test_fail& tf)
            {
                get_output() << "\tTest case " << std::setw(30) << std::left <<  t->test_name_ << " [FAILED].\n";
                t->teardown();
            }
        }

        return tests_passed == n_tests;
}

```

We essentially just run the collection function (remember that was std_vector_tests above), to add our tests to the test vector, and then run the tests. I used an exception on a failed test, because it made some things easier. I know that's a faux-pas. Let's take a look at an example that uses a fixture:

```cpp

#include "macroless.h"

#include <map>

// Do some tests on std::map.  We also take a look at text fixtures and a way to accomplish
// similar functionality just using the lambdas.

// Create test case vector for this test.
macroless::test_vector tests;

// Create something like a normal test-fixture.
// Test class.  Also serves as the base class for fixtures.
class map_test_fixture : public macroless::test
{
public:

    map_test_fixture(   std::string name,
                        std::function<bool(macroless::test*)> r,
                        std::function<void(macroless::test*)> su = [](macroless::test*){},
                        std::function<void(macroless::test*)> td = [](macroless::test*){}):
            macroless::test(name, r, su, td)
    {
    }

    virtual void setup()
    {
        macroless::get_output() << "\t\tSetting up map_test_fixture...\n";

        my_map_[4] = "C++";
        my_map_[-64] = "D";
        my_map_[0] = "Rust";

        macroless::test::setup();
    }
    virtual void teardown()
    {
        macroless::get_output() << "\t\tTearing down map_test_fixture...\n";

        macroless::test::teardown();
    }

    std::map<int,std::string> my_map_;
};

// Create collection function.
void std_map_tests()
{

    // Create test cases and add them to the test vector.
    // Test size of a vector.
    tests.push_back(
            macroless::test_ptr(
                    new map_test_fixture(
                            "map_size_check",
                            [](macroless::test* tst)
                            {
                                // We know we're dealing with a map_test_fixture here, so
                                // cast it.  A little more boilerplate...  We also have an additional
                                // level of indirection w.r.t. most testing frameworks.

                                map_test_fixture* this_tst =
                                        dynamic_cast<map_test_fixture*>(tst);

                                 if(this_tst->my_map_.size() != 3) {
                                     macroless::fail_test("my_map.size() != 3.");
                                 }

                                return true;
                            }
                    )));

    // Here's another similar idea to a fixture...

    // Create some big persistent resources.
    std::map<int, std::string> my_big_map;
    my_big_map[1] = "Oberon";
    my_big_map[18] = "Two Hearted";
    my_big_map[-1] = "Oarsman";

    // Test with my_big_map as capture.
    // TODO: there is a segfault here if my_big_map is captured by ref.
    // Need to think more?
    tests.push_back(
            macroless::test_ptr(
                    new macroless::test(
                            "check_for_key_28",
                            [my_big_map](macroless::test*)
                            {
                                if (my_big_map.find(28) == my_big_map.end()){
                                    macroless::fail_test("Key value 28 was not found in the map.");
                                }

                                // If we get here, we pass the test.
                                return true;
                            }
                    )));

    // Test with my_big_map as capture.
    tests.push_back(
            macroless::test_ptr(
                    new macroless::test(
                            "check_1_is_oberon",
                            [my_big_map](macroless::test*)
                            {
                                if (my_big_map.at(1) != "Oberon"){
                                    macroless::fail_test("my_big_map[1] != Oberon.");
                                }

                                // If we get here, we pass the test.
                                return true;
                            }
                    )));

}

// Entry point for test.
int main(int argc, char** argv) {
    return macroless::run(argc,argv,std_map_tests,tests);
}

```

We create a fixture by deriving something from macroless::test, and doing stuff in the setup and teardown functions. If we wanted, we could also add additional setup and teardown functionality per-test when we construct the test (or the fixture), basically in the same way the test is defined. This does the job, but at least with the code as is, we end up having to do an ugly dynamic cast, and we always have to do tst->... . Maybe there's a way around this, but I couldn't think of one quickly. Contrast that with e.g. Google Test. When you write a fixtured test with Google Test, you write the test as if you're "in the class". And I suspect, that is exactly what you're doing -- you're writing the virtual run function, and Google's macro TEST_F writes up the rest of the one-off type for you. I think the macroless experiment fails a bit here, or at least isn't as boilerplate free as the alternatives. However, by virtue of using "native" C++, we do potentially pick up some functionality. In the other non-fixtured tests defined above, we use lambda capture to copy some already-setup std::map object into the test. This provides some functionality somewhat similar to fixtures. With the full language at your disposal, I have a feeling there's a lot of other clever ways to cook up interesting tests.

### Conclusion

The goal here was to try to create a tiny C++ testing framework with NO\_MACROS. It was fun, and, the thing mostly works, but as I suspected, it reinforced the idea that the use of the macros in popular testing frameworks like Google Test and Catch are probably warranted. With those macros, writing a new case in an existing test is nearly zero-overhead, and writing a test case on a fixture is zero overhead, besides, of course, writing the fixture. I wasn't able to get macroless down to that level of boilerplate. In addition, I broke a few eggs of my own to get the job done. I used exceptions for control flow (again, not entirely sure that's needed), which is no-no probably on equal footing with over macro-ization. I also have that required dynamic cast for the fixtures. And use of modern C++ makes the framework unable to test legacy code. Still, it's interesting to have the whole language at your disposal when writing tests. For example, I know for sure that I could make a for loop that adds a test case each iteration, and at this moment, I'm not sure if I can do this with e.g., BOOST\_AUTO\_TEST\_CASE. In some sense, I just feel better reading a bit more C++ than a short and sweet macro -- at least at first. Separate from the macro issue, it's always interesting to what can be done in a few hundred lines of code. [macroless on github.](https://github.com/sgh1/macroless)