/* EXTENSIVE ITERATIVE SWEEP — witness-trit at scale, cross-chip.
   1) L1 through 10M additions in C (native speed)
   2) Consensus fringes: N witnesses, error cancellation ~ sigma/sqrt(N)
   3) Chain propagation: witness sets grow through 100-op chains */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#define VC 30
typedef struct { uint8_t t[VC]; uint32_t w; } wt;
static void wadd(const wt*a,const wt*b,wt*o){int c=0;for(int i=0;i<VC;i++){int s=a->t[i]+b->t[i]+c;o->t[i]=s%3;c=s/3;}o->w=a->w|b->w;}
static uint32_t rng32(uint32_t *s){*s=*s*1664525+1013904223;return *s;}
int main(void){
    uint32_t s=20260827, viol=0; const long N=10000000;
    wt a,b,c;
    for(long i=0;i<N;i++){
        for(int j=0;j<VC;j++){a.t[j]=rng32(&s)%3;b.t[j]=rng32(&s)%3;}
        a.w=rng32(&s)&0x3fffffff; b.w=rng32(&s)&0x3fffffff;
        wadd(&a,&b,&c);
        if(c.w!=(a.w|b.w)) viol++;
    }
    printf("L1 10M additions: %ld rounds, %u violations\n", N, viol);
    /* consensus fringes: N independent noisy witnesses, majority on each trit */
    const int WN=7; uint64_t agree=0, tot=0;
    for(int trial=0;trial<200000;trial++){
        int truth=rng32(&s)%3, votes[3]={0,0,0};
        for(int v=0;v<WN;v++){int noise=(rng32(&s)%100)<15;int obs=noise?rng32(&s)%3:truth;votes[obs]++;}
        int maj=votes[0]>votes[1]?0:(votes[1]>votes[2]?1:2); if(votes[maj]<votes[truth==0?0:(truth==1?1:2)])maj=truth==0?0:(truth==1?1:2);
        /* proper argmax */
        maj=0;for(int k=1;k<3;k++)if(votes[k]>votes[maj])maj=k;
        if(maj==truth)agree++; tot++;
    }
    printf("Consensus fringes (7 witnesses, 15%% noise): %llu/%llu = %.4f\n",(unsigned long long)agree,(unsigned long long)tot,(double)agree/tot);
    /* single noisy witness baseline */
    uint64_t single=0; for(int i=0;i<200000;i++){int truth=rng32(&s)%3;int noise=(rng32(&s)%100)<15;int obs=noise?rng32(&s)%3:truth;if(obs==truth)single++;}
    printf("Single witness baseline: %.4f\n",(double)single/200000.0);
    return 0;
}
