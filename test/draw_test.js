const TheHedgehog = artifacts.require("TheHedgehog");

const chai = require("./setupchai.js");
const BN = web3.utils.BN;
const assert = chai.assert;
const expect = chai.expect;

PRICE = new BN("30000000000000000");

contract("Test Draw", async accounts => {
    const [ initialHolder, recipient, anotherAccount ] = accounts;

    beforeEach(async () => {
        this.TheHedgehog = await TheHedgehog.deployed();
    });

    async function Buy(instance, recipient, n) {
        for (let i = 0; i < n / 20; ++i) {
            instance.mintTheHedgehog(new BN(20), {
                from: recipient,
                value: 20 * PRICE
            });
        }
    }

    it("INITIAL", async() => {
        let TheHedgehogInstance = this.TheHedgehog;
        Buy(TheHedgehogInstance, recipient, 20);
        Buy(TheHedgehogInstance, anotherAccount, 20);
        await expect(TheHedgehogInstance.balanceOf(recipient)).to.eventually.be.a.bignumber.equal(new BN("20"));
        await expect(TheHedgehogInstance.balanceOf(anotherAccount)).to.eventually.be.a.bignumber.equal(new BN("20"));

        
        let RecipientEth = new BN(await web3.eth.getBalance(recipient));
        let AnotherAccountEth = new BN(await web3.eth.getBalance(anotherAccount));

        //await TheHedgehogInstance.draw1({
        //    from: initialHolder
        //});
        
        let newRecipientEth = new BN(await web3.eth.getBalance(recipient));
        let newAnotherAccountEth = new BN(await web3.eth.getBalance(anotherAccount));

        let divRecipientEth = newRecipientEth.sub(RecipientEth);
        let divAnotherAccountEth = newAnotherAccountEth.sub(AnotherAccountEth);
        let truthPrize = divRecipientEth.add(divAnotherAccountEth);

        expect(truthPrize).to.be.a.bignumber.equal(new BN("6250000000000000000"));
        
    })
});