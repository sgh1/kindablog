---
title: Quick Introduction to multipole methods.
date: 2014.11.16
tags: mathematics
---
As someone who's more of a mathematics fan than a practitioner, multipole methods at first seemed like straight-up black magic to me. Problems that canonically have an $O(n^2)$ complexity being solved in $O(nlog(n))$ or $O(n)$ time seemed...like a lie. But I was able to get a grip on the simplest case, and now, I'm a believer. In this article, we won't outline a complete multipole algorithm, but we will aim to outline the cause or means of the reduced computational effort advertised by these types of algorithm.

#### Pre-Reqs:

There's not a whole lot of high-level concepts involved in understanding this article. And since you got here somehow, you probably already know them. Here's a short list of things you should be familiar with before going on:

*   Summation symbol and algebra
*   Taylor series & derivatives.
*   Very basic understanding of the N-body problem.

That's it!

#### The Problem:

We're trying to solve the [N-Body Problem](http://en.wikipedia.org/wiki/N-body_problem). Here's one example: we have N particles located in 1-D space, and each particle experiences a mutual interaction with all of the other particles. For each particle, you calculate the total interaction from other particles as: $$\psi(x_0) = \sum\limits_{i}^{N}f(x_0,x_i)*w_i \tag{1}$$ Where $f(x_0,x_i)$ defines the physical force or relationship between the observation point $x_0$, and the location of the particle, $x_i$. $w_i$ is some 'weight' for each particle. To solve the entire problem, this summation must be repeated N times -- so we have N*N operations. There's the $n^2$ complexity we seek to improve upon.

#### Something A Bit Different

Okay, now let's solve a slightly different problem. Say you have a small cloud or clump of particles near $x_d$, and you want to compute the force or response at $x_0$. You could re-write the interaction function like: $$f(x_0,x_i) = f(x_0,(x_i-x_d) + x_d)$$ All we did is sort of express $x_i$'s position as a distance from the cloud center, $x_d$. And now, we have to recall the only higher-math idea used in this article, the Taylor Series: $$f(x) = \sum\limits_{n=0}^{\infty}\frac{f^n(a)}{n!}(x-a)^n$$ The Taylor Series says that we can compute some function $f(x)$ by computing the above series about some point $a$. $f^n$ just means the 'nth' derivative of $f$. Using that same language, we could express our interaction function, $f(x_0,x_i) = f(x_0,(x_i-x_d) + x_d)$ with a Taylor Series about $x_d$: $$\psi(x,x_i) = \sum\limits_{n=0}^{\infty}\frac{f^n(x,x_d)}{n!}(x_i-x_d)^n$$ To compute the response or force at $x_0$ from the cloud of particles, like we did above, we would need to do a Taylor expansion (or series) for each point in the cloud: $$\psi(x) = \sum\limits_{i}^{N}\sum\limits_{n=0}^{\infty}\frac{f^n(x,x_d)}{n!}(x_i-x_d)^nw_i$$ Keep in mind that if we keep all the terms of the Taylor Series, this equation is exactly equivalent to (1). Here is where things start to get interesting. We can move a summation around to express what is dependent on the $i$ sum. Let's also truncate the Taylor Series. We'll use only the first 3 terms, so $M=2$. The mathematics for whether or not this is a 'good' approximation can be complicated, but it's a little beyond the scope of our ten-minute intro: $$\psi(x) = \sum\limits_{n=0}^{M}\frac{f^n(x,x_d)}{n!}\sum\limits_{i=0}^{N}(x_i-x_d)^nw_i \tag{2}$$ That's a good approximation for $\psi(x)$, but what does that get us? Look again at this summation: $\sum\limits_{i=0}^{N}(x_i-x_d)^nw_i$. There is no dependence at all on our observation point, $x_0$! Each of the $n = 0,1,2,...,N$ terms only depend on the cloud itself. You could have computed these $n$ terms before I told you where $x0$ was to be. And if I gave you a different $x_0$, you could re-use these terms. We could re-write (2) as: $$\psi(x_0) = \sum\limits_{n=0}^{\infty}\frac{f^n(x_0,x_d)}{n!} T_n$$ Which tells us if we needed compute another $\psi(x_0)$, we only need to do 3 further operations.

#### The Payoff:

If we had a cloud of $N=1,000$ particles, with, say, $k = 100$ observation points outside of the cloud, we would need to do $N*(M+1)$ evaluations of $f$ to get the coefficients $T_n$, and then another $(k-1)*(M+1)$ computations to compute the response at the observation points. That'd be 3300 evaluations of $f$ for this case. For the original equation (1), we'd need to do $N*k$ evaluations, or 100,000 for this case. That's a factor of 30! It's a little more work to prove the complexity exactly, but we can see it is alreay much better than $n^2$.

#### MATLAB Code:

Here is a small matlab code to compute the response from a particle cloud for a few observations points. The response is also computed in the normal way for comparison. In this code, $f(x_0,x_i) = \frac{1}{|x_0 - x_i|)}$. As described above, this is the krux of our multi-pole algorithm.

```matlab
clear all;

%observation locations
x0 = [-10,-50,25];

%center of cloud
xC = -100;

%particles in cloud
n = 250;

%taylor order + 1
M = 6;

%precompute factorials
Mfact = [1,1,2,6,24,factorial(5)];

%generate the point cloud
xCa = rand(1,n) + xC;

%normal method, interaction function is f = 1/r
sum1 = zeros( length(x0),1 );
for y = 1:length(x0)
	for k = 1:n
		sum1(y) = sum1(y) + (1 / (abs( x0(y)-xCa(k) ) ) );
	end
end

disp("response as computed normally:");
disp(sum1);

%compute Taylor coefficients, assume a fixed weight of 1
%this only needs to be done once!
moment = zeros(1,M);

for m = 1:M
	for k = 1:n
		moment(m) = moment(m) + (xCa(k) - xC)^(m-1);
	end
end

%now compute the (approximate) interaction
sum2 = zeros( length(x0),1 );
for y = 1:length(x0)
	for k = 1:M
		sum2(y) = sum2(y) + ( (-1)^(k-1) / (abs( x0(y)-xC ) )^k ) * (1/Mfact(k)) * moment(k);
	end
end

disp("multipole responses:");
disp(sum2);

disp("errors:");
disp(abs(sum1-sum2));

```

#### Back to the Original Problem

In the section above, we showed how we could compute the interaction between many observation points away from a cluster or cloud of particles in a way where many evaluations of the interaction function, $f$, can be re-used. In fact, at the heart of many multipole methods is some type of re-use similar to that explained above. Remember, though, that our original goal was to solve the N-body problem, where we compute the mutual interaction of $N$ particles. Finding a way to compute the interaction between a particle at $x_0$, and the rest of the particles might force us to revert to the normal interaction equation for particles that are close to $x_0$. Luckily, this number might be much smaller than the number of particles far way from the particle, which we can gather into clouds, for which the method described above could be used. More work is certainly involved to create a fully-functional multipole code, but hopefully this article describes where a lot of the speedup comes from.

#### Sources

*   [A Fast Algorithm for Particle Simulations](https://galton.uchicago.edu/~lekheng/courses/302/classics/greengard-rokhlin.pdf) -- L. GREENGARD AND V.ROKHLIN (one of the original papers on the subject).
*   [A treecode algorithm for simulating electron dynamics in a Penning–Malmberg trap](http://www.math.lsa.umich.edu/~krasny/paper_cpc_2004.pdf) -- A.J. Christlieb et. al (very clear paper, and directly inspired this article)!